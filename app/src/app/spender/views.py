from django.shortcuts import render

from app.common import get_logger
from app.spender.models import Transaction


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
