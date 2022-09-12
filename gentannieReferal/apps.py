from django.apps import AppConfig


class GentanniereferalConfig(AppConfig):
    name = 'gentannieReferal'

    def ready(self):
        from . import signals
