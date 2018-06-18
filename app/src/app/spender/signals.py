from django.dispatch import receiver

from app.records.models import Record
from app.records.signals import ready_to_process
from app.common import get_logger
from .models import Transaction


log = get_logger(__file__)


ALLOWED_RECORD_LABELS = ('income', 'costs')


def get_amount_currency_dir(record_instance):

    currency_entities = []
    number_entities = []

    for entity in record_instance.entities.all():
        if entity.name == 'CurrencyEntity':
            currency_entities.append(entity.entity_attrs)
        elif entity.name in ('NumberEntity', 'NumberWithThousandEntity'):
            number_entities.append(entity.entity_attrs)

    if not currency_entities and not number_entities:
        raise ValueError('No entities')

    direction = 0 if record_instance.label == 'income' else 1
    currency = None

    if currency_entities:
        entity = currency_entities[0]
        currency = entity['currency']
    elif number_entities:
        number_entities.sort(key=lambda it: it['value'], reverse=True)
        entity = number_entities[0]

    return (entity['value'], currency, direction)


@receiver(ready_to_process, sender=Record)
def record_saved(sender, instance, **kwargs):

    log.debug('Signal: %s with instance: %s', sender, instance)

    transaction = None

    # Вдруг изменился label
    try:
        transaction = Transaction.objects.get(record=instance)
        if instance.label not in ALLOWED_RECORD_LABELS:
            transaction.delete()
            return None
    except Transaction.DoesNotExist:
        pass

    if instance.label not in ALLOWED_RECORD_LABELS:
        log.debug('Label %s not aplicable', instance.label)
        return None

    try:
        amount, currency, direction = get_amount_currency_dir(instance)

        if transaction is None:
            Transaction.create_transaction(
                instance, amount, direction, currency=currency)
        else:
            transaction.edit_transaction(amount, direction, currency=currency)
    except ValueError as exc:
        log.debug(str(exc))
