from django.apps import AppConfig


class SpenderConfig(AppConfig):

    name = 'app.spender'

    def ready(self):

        from . import signals
