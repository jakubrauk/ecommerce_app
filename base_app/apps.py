from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_app'

    def ready(self):
        from .signals import create_groups_permissions
        post_migrate.connect(create_groups_permissions, sender=self)


