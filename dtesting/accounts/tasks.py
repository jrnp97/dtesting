from dtesting.celery import app # Crea una dependencia con tu proyecto principal

from celery import shared_task # NO Te crea dependencia con tu proyecto principal.

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
