from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin, FormValidMessageMixin, AnonymousRequiredMixin, MessageMixin
from braces.views._access import AccessMixin
from vanilla import UpdateView, CreateView, TemplateView

from .forms import UpdateEmailForm, ProfileForm, UserForm
from .models import Nutzerprofil


class RedirectMixin:
    """Mixin for looking for 'next'-parameter in GET"""
    def get_success_url(self):
        return self.request.GET.get('next') or super().get_success_url()


class CreateUserView(AnonymousRequiredMixin, CreateView):
    """ erstellt einen Nutzerzugang, nur eMail und Passwort """
    form_class = UserForm
    template_name = 'Nutzer/registrieren.html'
    success_url = reverse_lazy('Nutzer:mail_wurde_versandt')
    authenticated_redirect_url = reverse_lazy('Nutzer:profil')


class CreateProfileView(AnonymousRequiredMixin, RedirectMixin, MessageMixin, CreateView):
    """ für später, wenn die Profilinfos mal sowieso notwendig sind und
    einen nackten Nutzer zu erstellen nicht zulässig sein soll """
    form_class = UserForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('Nutzer:profil')
    authenticated_redirect_url = reverse_lazy('Nutzer:profil')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST)
        else:
            context['profile_form'] = ProfileForm()
        return context

    def form_valid(self, form):
        profile_form = ProfileForm(self.request.POST)
        if profile_form.is_valid():
            user = form.save(profile_kwargs=profile_form.cleaned_data)
            self.messages.info('Profil gespeichert')
            self.request.session['updated'] = user.profile.pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'Nutzer/meine_daten.html'
    form_valid_message = 'Profil gespeichert'
    login_url = '/auth/anmelden/'
    success_url = reverse_lazy('Nutzer:meine_daten')

    def get_object(self):
        return self.request.user.profil

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session['updated'] = self.object.pk
        return response


class UpdateEmailView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    form_class = UpdateEmailForm
    template_name = 'Nutzer/formular_mail_aendern.html'
    success_url = reverse_lazy('Nutzer:meine_daten')
    form_valid_message = 'Email-Adresse gespeichert'

    def get_object(self):
        return self.request.user
