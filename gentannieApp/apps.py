from django.apps import AppConfig


class GentannieappConfig(AppConfig):
    name = 'gentannieApp'

    # def ready(self):
    #     from . import signals

    def ready(self):
        from . import updater
        updater.start()