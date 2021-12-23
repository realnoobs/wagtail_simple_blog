from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SimpleBlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "simple_blog"
    verbose_name = "Simple Blog"

    def ready(self):
        post_migrate.connect(init_app, sender=self)


def init_app(*args, **kwargs):
    pass
