import logging
logger = logging.getLogger(__name__)

from captcha.fields import ReCaptchaField
from django import forms
from django.conf import settings

from django.contrib.auth import get_user_model
from .models import Nutzerprofil


class UserForm(forms.ModelForm):
    if not settings.DISABLE_CAPTCHA:
        captcha = ReCaptchaField(attrs={'_no_label': True, '_no_errors': True})

    class Meta:
        model = get_user_model()
        fields = ['email']

    def save(self, commit=True, profile_kwargs={}):
        """Sends out email with pw reset link if user is created."""
        nutzer = super().save(commit=commit)
        if commit:
            Nutzerprofil.objects.create(nutzer=nutzer, **profile_kwargs)
            logger.info('Nutzerprofil für {} erstellt'.format(nutzer))
            nutzer.send_activation_mail()
        return nutzer


class UpdateEmailForm(forms.ModelForm):
    password = forms.CharField(label='Bestätigen Sie Ihr Passwort', widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.instance.check_password(password):
            raise forms.ValidationError('Invalid password')
        return password

    class Meta:
        model = get_user_model()
        fields = ['email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Nutzerprofil
        #fields = ['anrede', 'vorname', 'nachname', 'strasse', 'plz', 'stadt']
        exclude = ['nutzer']

        # Layout used by django-semanticui
        layout = [
            ("Three Fields",
                ("Field", "anrede"),
                ("Field", "vorname"),
                ("Field", "nachname")),
            ("Three Fields",
                ("Field", "strasse"),
                ("Field", "plz"),
                ("Field", "stadt")),
        ]
