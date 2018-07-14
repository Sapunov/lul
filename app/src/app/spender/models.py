from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

from app.records.models import Record
from app.spender.misc import split_float


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=400, default='', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)

    @classmethod
    def get_user_and_common(cls, user):

        categories = cls.objects.filter(
            Q(owner=user) | Q(owner__isnull=True))

        return categories

    def __str__(self):

        return '<Category: {0},{1}>'.format(
            self.name,
            'None' if self.owner is None else self.owner.username)

    def __repr__(self):

        return self.__str__()


class Transaction(models.Model):

    DIRECTIONS = (
        (0, 'income'),
        (1, 'expense')
    )

    amount_int = models.IntegerField()
    amount_decimal = models.IntegerField()
    currency = models.CharField(max_length=10, default=settings.DEFAULT_CURRENCY)
    direction = models.SmallIntegerField(choices=DIRECTIONS)
    category = models.ForeignKey(Category,  null=True, on_delete=models.SET_NULL, related_name='transactions')
    category_confirmed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name='+')

    def create(self, *args, **kwargs):

        raise ValueError('User `create_transaction` instead of this method')

    @classmethod
    def create_transaction(cls, record, amount, direction, currency=None):

        integer_, decimal_ = split_float(amount)
        currency = currency if currency is not None else settings.DEFAULT_CURRENCY
        direction = 0 if direction == 'income' else 1

        return cls.objects.create(
            record=record,
            amount_int=integer_,
            amount_decimal=decimal_,
            direction=direction,
            currency=currency,
            timestamp=record.timestamp,
            owner=record.owner)

    def edit_transaction(self, amount, direction, currency=None):

        integer_, decimal_ = split_float(amount)
        currency = currency if currency is not None else settings.DEFAULT_CURRENCY
        direction = 0 if direction == 'income' else 1

        self.amount_int = integer_
        self.amount_decimal = decimal_
        self.direction = direction
        self.currency = currency

        self.save()

    @property
    def amount(self):

        return self.amount_int + self.amount_decimal / 10000

    @property
    def direction_human(self):

        return Transaction.DIRECTIONS[self.direction][1]

    @property
    def category_variants(self):

        categories = Category.get_user_and_common(self.owner)
        return categories
