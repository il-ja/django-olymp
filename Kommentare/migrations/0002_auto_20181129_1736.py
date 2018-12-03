# Generated by Django 2.1 on 2018-11-29 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Kommentare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kommentar',
            name='autor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kommentare', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='kommentar',
            name='liste',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kommentare', to='Kommentare.Liste'),
        ),
    ]
