# Generated by Django 2.1 on 2018-12-04 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nutzer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutzerprofil',
            name='anrede',
            field=models.CharField(choices=[('m', 'Herr'), ('w', 'Frau'), ('', 'N/A')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='nutzerprofil',
            name='farbschema',
            field=models.CharField(choices=[('/static/Grundgeruest/css/w3-theme-amber.css', 'Zeus'), ('/static/Grundgeruest/css/w3-theme-blue.css', 'Poseidon'), ('/static/Grundgeruest/css/w3-theme-indigo.css', 'Hera'), ('/static/Grundgeruest/css/w3-theme-brown.css', 'Demeter'), ('/static/Grundgeruest/css/w3-theme-yellow.css', 'Apollo'), ('/static/Grundgeruest/css/w3-theme-light-green.css', 'Artemis'), ('/static/Grundgeruest/css/w3-theme-dark-grey.css', 'Athene'), ('/static/Grundgeruest/css/w3-theme-red.css', 'Ares'), ('/static/Grundgeruest/css/w3-theme-pink.css', 'Aphrodite'), ('/static/Grundgeruest/css/w3-theme-grey.css', 'Hermes'), ('/static/Grundgeruest/css/w3-theme-orange.css', 'Hephaistos'), ('/static/Grundgeruest/css/w3-theme-cyan.css', 'Dionysus')], default='/static/Grundgeruest/css/w3-theme-dark-grey.css', max_length=255),
        ),
    ]
