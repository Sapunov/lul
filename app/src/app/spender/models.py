from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from app.records.models import Record
from app.spender.misc import split_float


class Transaction(models.Model):

    DIRECTIONS = (
        (0, 'income'),
        (1, 'expense')
    )

    amount_int = models.IntegerField()
    amount_decimal = models.IntegerField()
    currency = models.CharField(max_length=10, default=settings.DEFAULT_CURRENCY)
    direction = models.SmallIntegerField(choices=DIRECTIONS)
    category = models.CharField(max_length=50, blank=True, null=True)
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
