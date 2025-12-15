from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={"max_retries": 3},
)
def send_note_email(self, email, title, action):
    send_mail(
        subject=f"Note {action}",
        message=f"Your note '{title}' was {action.lower()} successfully.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f"Note email sent to {email}"
