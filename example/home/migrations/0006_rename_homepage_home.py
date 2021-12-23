# Generated by Django 3.2.10 on 2021-12-23 12:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailsearchpromotions', '0002_capitalizeverbose'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailimages', '0023_add_choose_permissions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0005_auto_20211223_1156'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePage',
            new_name='Home',
        ),
    ]