from django.apps import AppConfig


class SpenderConfig(AppConfig):

    name = 'logulife.spender'

    def ready(self):

        from . import signals
