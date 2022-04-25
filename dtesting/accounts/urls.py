from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import test_celery, CustomLoginView, success_login, in_progress_url, in_progress_url_two

app_name = 'accounts'
urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('celery/', test_celery, name='testing_celery'),
    path('lsuccess/', success_login, name='success_login'),
    path('inp/', in_progress_url, name='p'),
    path('inp2/', in_progress_url_two, name='p2'),
]

# Otra posible solucion es desglozandola, es decir definiendo todas las urls de authenticacion manualmente.
# ref: https://docs.djangoproject.com/en/4.0/topics/auth/default/#module-django.contrib.auth.views
