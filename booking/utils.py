from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
def send_notification_to_technician(technician_email, mail_subject, mail_template, user):

    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, {'user': user})
    mail = EmailMessage(mail_subject, message, from_email, to=[technician_email])
    mail.content_subtype = 'html'
    mail.send()

def send_notification_to_user(user_email, mail_subject, mail_template, user):

    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, {'user': user})
    mail = EmailMessage(mail_subject, message, from_email, to=[user_email])
    mail.content_subtype = 'html'
    mail.send()