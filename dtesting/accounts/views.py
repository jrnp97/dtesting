from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
# Create your views here.
from django.urls import reverse_lazy

from .tasks import new_login_detected, no_registered


class CustomLoginView(LoginView):
    template_name = 'accounts/my_login.html'
    success_url = reverse_lazy('accounts:success_login')

    def form_valid(self, form):
        """ Overriding form_valid to perform custom actions after login"""
        auth_login(self.request, form.get_user())
        print("ENVIANDO EMAIL")
        new_login_detected.delay(user_id=form.get_user().id)
        return HttpResponseRedirect(self.get_success_url())


@login_required
def success_login(request):
    # Como yo puedo saber que la view esta siendo invocada por causa de un login exitoso.
    print("SUCCESS_VIEW_EXECUTE")
    return HttpResponse(content=f'You are logged!, {request.user}!')


@login_required
def test_celery(request):
    return HttpResponse(content='JAJA')
