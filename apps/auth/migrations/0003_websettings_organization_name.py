# Generated by Django 3.2.10 on 2021-12-24 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_websettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='websettings',
            name='organization_name',
            field=models.CharField(blank=True, help_text='Your company, community or your name.', max_length=255, null=True, verbose_name='organization name'),
        ),
    ]
