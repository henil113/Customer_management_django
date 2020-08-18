from django.apps import AppConfig


class Filedata9Config(AppConfig):
    name = 'filedata9'

    def ready(self):
        import filedata9.signals
