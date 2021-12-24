from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from wagtail.contrib.settings.models import BaseSetting, register_setting


class User(AbstractUser):
    pass


class Preference(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)


@register_setting
class WebSettings(BaseSetting):
    logo = models.ImageField(verbose_name=_("logo"), help_text=_("Logo image for header, footer etc."))
    organization_name = models.CharField(
        verbose_name=_("organization name"),
        max_length=255, null=True, blank=True,
        help_text=_("Your company, community or your name."),
    )
