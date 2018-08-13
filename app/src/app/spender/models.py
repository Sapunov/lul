from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
import pytz
import requests

from app.records.models import Record
from app.spender.misc import split_float
from app.common import get_logger


log = get_logger(__name__)


DIRECTIONS = (
    (0, 'income'),
    (1, 'expense')
)


class Category(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400, default='', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
    direction = models.SmallIntegerField(choices=DIRECTIONS)

    @classmethod
    def get_user_and_common(cls, user):

        categories = cls.objects.filter(
            Q(owner=user) | Q(owner__isnull=True))

        return categories

    @property
    def direction_human(self):

        return DIRECTIONS[self.direction][1]

    def __str__(self):

        return '<Category: {0},{1}>'.format(
            self.name,
            'None' if self.owner is None else self.owner.username)

    def __repr__(self):

        return self.__str__()


class ExchangeRate(models.Model):

    base = models.CharField(max_length=5)
    symbol = models.CharField(max_length=5)
    date = models.DateField()
    rate = models.FloatField()

    class Meta:
        indexes = [
            models.Index(fields=['symbol']),
            models.Index(fields=['date'])
        ]

    @classmethod
    def download_rates(cls, date):

        formatted_date = date.strftime('%Y-%m-%d')

        try:
            req = requests.get(
                settings.FIXER['url'].format(
                    date=formatted_date,
                    access_key=settings.FIXER['access_key']),
                timeout=settings.FIXER['timeout'])

            log.debug('Received response from Fixer: {0}'.format(req))

            if req.ok:
                data = req.json()
                rates = data['rates']
                base = data['base'].lower()
                items = []
                for code, rate in rates.items():
                    items.append(
                        cls(
                            base=base,
                            symbol=code.lower(),
                            date=datetime(date.year, date.month, date.day, tzinfo=pytz.utc),
                            rate=rate))
                cls.objects.bulk_create(items)
        except (requests.RequestException, requests.exceptions.ConnectionError) as e:
            log.exception(e)

    @classmethod
    def get_rates(cls, date, *symbols):

        if len(symbols) == 1 and isinstance(symbols[0], (list, tuple)):
            symbols = symbols[0]

        rates = cls.objects.filter(symbol__in=symbols, date=date)

        if not rates.exists():
            cls.download_rates(date)

        rates = cls.objects.filter(symbol__in=symbols, date=date)

        if not rates.exists():
            raise ValueError('Rates not found')

        base = set(it.base for it in rates)

        assert len(base) == 1, 'Bad base'

        base = list(base)[0]

        ans = {}
        for rate in rates:
            ans[rate.symbol] = rate.rate

        return base, date, ans

    @classmethod
    def convert(cls, code_from, code_to, amount, date):

        log.debug('Converting amount=%s from %s to %s with date=%s',
            amount, code_from, code_to, date)

        try:
            _, _, rates = cls.get_rates(date, code_from, code_to)
        except ValueError:
            return None

        log.debug('Rates: %s', rates)

        rate_from = rates[code_from]
        rate_to = rates[code_to]

        converted_amount = (amount / rate_from) * rate_to

        log.debug('Converting result %s->%s', amount, converted_amount)

        return converted_amount

    def __str__(self):

        return '<ExchangeRate base={0} symbol={1} rate={2} date={3}>'.format(
            self.base, self.symbol, self.rate, self.date)

    def __repr__(self):

        return self.__str__()


class Transaction(models.Model):

    amount_int = models.IntegerField()
    amount_decimal = models.IntegerField()
    currency = models.CharField(max_length=10, default=settings.DEFAULT_CURRENCY)
    direction = models.SmallIntegerField(choices=DIRECTIONS)
    category = models.ForeignKey(Category,  null=True, on_delete=models.SET_NULL, related_name='transactions')
    category_confirmed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='+')
    _default_currency = models.CharField(max_length=10)
    default_currency_amount_int = models.IntegerField(null=True)
    default_currency_amount_decimal = models.IntegerField(null=True)

    @classmethod
    def filter_transactions(cls, owner, q=None, timestamp_from=None,
            timestamp_to=None, tags=None, categories=None):

        filters = {}

        if q is not None:
            filters['record__text__icontains'] = q

        if timestamp_from is not None:
            filters['timestamp__gte'] = timestamp_from

        if timestamp_to is not None:
            filters['timestamp__lte'] = timestamp_to

        transactions = cls.objects.filter(owner=owner, **filters)

        return transactions

    def create(self, *args, **kwargs):

        raise ValueError('User `create_transaction` instead of this method')

    @classmethod
    def create_transaction(cls, record, amount, direction, currency=None):

        integer_, decimal_ = split_float(amount)
        currency = currency if currency is not None else settings.DEFAULT_CURRENCY
        direction = 0 if direction == 'income' else 1

        transaction = cls.objects.create(
            record=record,
            amount_int=integer_,
            amount_decimal=decimal_,
            direction=direction,
            currency=currency,
            _default_currency=settings.DEFAULT_CURRENCY,
            default_currency_amount_int=None,
            default_currency_amount_decimal=None,
            timestamp=record.timestamp,
            owner=record.owner)

        transaction.calc_default_currency()

        return transaction

    def edit_transaction(self, amount, direction, currency=None):

        integer_, decimal_ = split_float(amount)
        currency = currency if currency is not None else settings.DEFAULT_CURRENCY
        direction = 0 if direction == 'income' else 1

        self.amount_int = integer_
        self.amount_decimal = decimal_
        self.direction = direction
        self.currency = currency
        self._default_currency = settings.DEFAULT_CURRENCY

        self.save()

        self.calc_default_currency()

    def calc_default_currency(self):

        if self.currency != self._default_currency:
            converted_amount = ExchangeRate.convert(
                self.currency,
                self._default_currency,
                self.amount,
                self.timestamp)

            if converted_amount is not None:
                converted_amount_int, converted_amount_decimal = split_float(
                    converted_amount)

                self.default_currency_amount_int = converted_amount_int
                self.default_currency_amount_decimal = converted_amount_decimal
                self.save()

    @property
    def amount(self):

        return self.amount_int + self.amount_decimal / 10000

    @property
    def default_currency(self):

        amount = self.amount

        if (self._default_currency != self.currency) and \
                not (self.default_currency_amount_int is None \
                or self.default_currency_amount_decimal is None):
            amount = self.default_currency_amount_int + self.default_currency_amount_decimal / 10000

            return {
                'amount': round(amount, 2),
                'currency': self._default_currency
            }

        return None

    @property
    def direction_human(self):

        return DIRECTIONS[self.direction][1]

    @property
    def category_variants(self):

        categories = Category.get_user_and_common(self.owner)
        return categories
