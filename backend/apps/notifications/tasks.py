from celery import shared_task
from .emailing import send_templated_email

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_email_task(self, recipient, subject, template_name, context):
    return send_templated_email(
        recipient=recipient,
        subject=subject,
        template_name=template_name,
        context=context,
    )
