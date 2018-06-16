from django.shortcuts import render

from logulife.common import get_logger


log = get_logger(__file__)


def record_create(record_obj):

    log.debug('Record created: %s', record_obj)


def record_update(record_obj):

    log.debug('Record updated: %s', record_obj)


def record_delete(record_id):

    log.debug('Record with id=%s deleted', record_id)
