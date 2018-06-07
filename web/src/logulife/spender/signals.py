from django.dispatch import receiver

from logulife.api.models import Record
from logulife.api.signals import ready_to_process
from logulife.common import get_logger
from .models import Transaction


log = get_logger(__file__)


@receiver(ready_to_process, sender=Record)
def record_saved(sender, instance, **kwargs):

    log.debug('Signal: %s with instance: %s', sender, instance)

    if instance.label not in ('income', 'costs'):
        log.debug('Label %s not aplicable', instance.label)
        return None

    currency_entities = []
    number_entities = []

    for entity in instance.entities.all():
        if entity.name == 'CurrencyEntity':
            currency_entities.append(entity.entity_attrs)
        elif entity.name in ('NumberEntity', 'NumberWithThousandEntity'):
            number_entities.append(entity.entity_attrs)

    if currency_entities:
        entity = currency_entities[0]
        Transaction.create_transaction(
            instance,
            entity['value'],
            0 if instance.label == 'income' else 1,
            currency=entity['currency'])
    elif number_entities:
        number_entities.sort(key=lambda it: it['value'], reverse=True)
        entity = number_entities[0]
        Transaction.create_transaction(
            instance,
            entity['value'],
            0 if instance.label == 'income' else 1)
