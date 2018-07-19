from django.conf import settings
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from app.common import get_logger
from app.spender.models import Transaction, Category
from app.spender.serializers import (
    CategorySerializer, TransactionSerializer, CategoryDeleteSerializer,
    CategorySetSerializer, CategoryIdSerializer)


ALLOWED_LABELS = ('income', 'expence')

log = get_logger(__file__)


def amount_and_currency(record_instance):

    currency_entities = []
    number_entities = []

    for entity in record_instance.entities.all():
        if entity.name == 'CurrencyEntity':
            currency_entities.append(entity)
        elif entity.name in ('NumberEntity', 'NumberWithThousandEntity'):
            number_entities.append(entity)

    if not currency_entities and not number_entities:
        raise ValueError('No entities')

    currency = None

    if currency_entities:
        entity = currency_entities[0]
        currency = entity.entity_attrs['currency']
    else:
        number_entities.sort(key=lambda it: float(it.value), reverse=True)
        entity = number_entities[0]

    return (float(entity.value), currency)


def record_create(record_obj):

    log.debug('Call record_created: %s', record_obj)

    if record_obj.label not in ALLOWED_LABELS:
        log.debug('Label of record is %s. Pass...', record_obj.label)
        return

    try:
        amount, currency = amount_and_currency(record_obj)
        Transaction.create_transaction(
            record_obj, amount, record_obj.label, currency)
    except ValueError as exc:
        log.debug(exc)


def record_update(record_obj):

    log.debug('Call record_update: %s', record_obj)

    if not Transaction.objects.filter(record=record_obj).exists():
        return record_create(record_obj)

    transaction = Transaction.objects.get(record=record_obj)

    if record_obj.label not in ALLOWED_LABELS:
        log.debug('Label of record is %s. Deleting...', record_obj.label)
        transaction.delete()
        return

    try:
        amount, currency = amount_and_currency(record_obj)
        transaction.edit_transaction(amount, record_obj.label, currency)
    except ValueError as exc:
        log.debug('Unable to extract amount. Deleting...')
        transaction.delete()


def record_delete(record_id):

    log.debug('Record with id=%s deleted', record_id)
    try:
        transaction = Transaction.objects.get(record__id=record_id)
        transaction.delete()
    except Transaction.DoesNotExist:
        log.debug('No transaction with record=%s. Do nothing...', record_id)


class CategoriesView(GenericAPIView):

    serializer_class = CategorySerializer

    def get(self, request):

        categories = Category.get_user_and_common(request.user)
        queryset = self.paginate_queryset(categories)

        serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

class CategoryDeleteView(GenericAPIView):

    serializer_class = CategoryDeleteSerializer

    def delete(self, request, cat_id):

        data = {
            'id': cat_id
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        category = serializer.validated_data['category']
        for transaction in category.transactions.all():
            transaction.category_confirmed = False
            transaction.save()
        category.delete()

        return Response({'deleted': True})


class TransactionsView(GenericAPIView):

    serializer_class = TransactionSerializer

    def get(self, request):

        params = request.query_params
        filters = {}

        if 'q' in params:
            filters['record__text__icontains'] = params['q']

        transactions = Transaction.objects.filter(
            owner=request.user, **filters).order_by('-timestamp')
        queryset = self.paginate_queryset(transactions)

        serializer = self.get_serializer(queryset, many=True)

        return self.get_paginated_response(serializer.data)


class CategorySetView(GenericAPIView):

    serializer_class = CategorySetSerializer

    def post(self, request, transaction_id, category_id):

        data = {
            'transaction_id': transaction_id,
            'category_id': category_id
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        transaction = serializer.validated_data['transaction']
        category = serializer.validated_data['category']

        transaction.category = category
        transaction.category_confirmed = True
        transaction.save()

        return Response()


class CategoryConfirmView(GenericAPIView):

    serializer_class = CategoryIdSerializer

    def post(self, request, transaction_id):

        data = {
            'transaction_id': transaction_id
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        transaction = serializer.validated_data['transaction']

        transaction.category_confirmed = True
        transaction.save()

        return Response()
