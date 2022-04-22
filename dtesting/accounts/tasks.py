from dtesting.celery import app # Crea una dependencia con tu proyecto principal
from celery import shared_task # NO Te crea dependencia con tu proyecto principal.

from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()


@app.task
def success_register_email_task():
    pass


@shared_task
def test_task_account():
    return 1 + 2


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def new_login_detected(user_id: int) -> bool:
    """
    Task to send a new login email notification to user.
    """
    # if not type(user_id) == int:
    # if not type(user_id) is int: <-
    if not isinstance(user_id, int) or user_id < 0:
        raise TypeError("Invalid `user_id` type.")
    user = User.objects.get(id=user_id)
    delivery_messages = send_mail(
        subject='New Login Detected.',
        message='A New login was detected in tijuana.',
        from_email='no-reply@google.com',
        recipient_list=[
            user.email,
        ],
        fail_silently=False,
    )
    return delivery_messages == 1

