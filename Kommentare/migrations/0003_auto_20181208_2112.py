# Generated by Django 2.1.4 on 2018-12-08 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kommentare', '0002_auto_20181129_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kommentar',
            name='text',
            field=models.TextField(),
        ),
    ]