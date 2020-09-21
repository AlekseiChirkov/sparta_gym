from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'users'

    def ready(self):
        from . import signals
