# Generated by Django 2.2.5 on 2019-09-03 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscribers', '0002_auto_20190903_0628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriber',
            options={'verbose_name': 'Subscriber', 'verbose_name_plural': 'Subscribers'},
        ),
    ]