from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'accounts/my_login.html'


@login_required
def test_celery(request):
    return HttpResponse(content='JAJA')
