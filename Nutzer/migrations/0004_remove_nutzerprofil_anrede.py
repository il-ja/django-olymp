# Generated by Django 2.1.4 on 2018-12-12 23:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Nutzer', '0003_auto_20181208_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nutzerprofil',
            name='anrede',
        ),
    ]
