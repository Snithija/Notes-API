from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_note_email(email, title, action):
    send_mail(
        subject=f"Note {action}",
        message=f"Your note '{title}' was {action.lower()} successfully.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )
