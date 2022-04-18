from django.urls import path, include

from .views import test_celery
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('celery/', test_celery, name='testing_celery')
]
