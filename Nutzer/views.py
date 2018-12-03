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


#class UpdateOrCreateRequiredMixin(MessageMixin):
#    """
#    Saves (and restores) GET parameters to session and returns view to create or update profile before continuing.
#    Resets after first retrieve of user.
#    """
#    def get(self, request, *args, **kwargs):
#        """Return update if session doesn't contain current user, marked as updated."""
#        profile_pk = request.session.get('updated')
#        if not profile_pk or (request.user.is_authenticated and request.user.profile.pk != profile_pk):
#            # Save params to session
#            request.session['get_params'] = request.GET.dict()
#
#            if request.user.is_authenticated:
#                redirect_url = reverse('users:update')
#                self.messages.info('Bitte bestätigen Sie Ihre Profilinformationen')
#            else:
#                redirect_url = reverse('users:create')
#            return HttpResponseRedirect('{}?next={}'.format(redirect_url, request.path_info))
#
#        # Pop url params and add to GET
#        get_params = request.session.pop('get_params', {})
#        request.GET = request.GET.copy()
#        request.GET.update(get_params)
#        return super().get(request, *args, **kwargs)
#
#    def get_profile(self):
#        """Returns updated user profile and removes session variable."""
#        profile_pk = self.request.session.pop('updated', None)
#        if self.request.user.is_authenticated and self.request:
#            return self.request.user.profile
#        if profile_pk:
#            return Profile.objects.get(pk=profile_pk)


class CreateUserView(AnonymousRequiredMixin, CreateView):
    form_class = UserForm
    template_name = 'Nutzer/registrieren.html'
    success_url = reverse_lazy('Nutzer:signup_complete')
    authenticated_redirect_url = reverse_lazy('Nutzer:profil')


class CreatedUserView(TemplateView):
    template_name = 'registration/signup_complete.html'


class CreateProfileView(AnonymousRequiredMixin, RedirectMixin, MessageMixin, CreateView):
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


class UpdateProfileView(RedirectMixin, ProfileView):
    template_name = 'users/profile_form.html'


class UpdateEmailView(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    form_class = UpdateEmailForm
    template_name = 'users/email_form.html'
    success_url = reverse_lazy('Nutzer:profil')
    form_valid_message = 'Email-Adresse gespeichert'

    def get_object(self):
        return self.request.user
