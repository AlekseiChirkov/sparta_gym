from django.apps import AppConfig


class ShopConfig(AppConfig):
    name = 'shop'
    verbose_name = 'Магазин и абонементы'

    def ready(self):
        from . import signals
