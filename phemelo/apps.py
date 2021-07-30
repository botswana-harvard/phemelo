from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'phemelo'
    verbose_name = 'Phemelo'
