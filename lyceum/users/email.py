import django.conf
import django.contrib
import django.contrib.auth
import django.contrib.auth.decorators
import django.core.mail
import django.shortcuts
import django.template.loader
import django.urls
import django.utils


__all__ = []


def send_user_email(username, email, template):
    html_content = django.template.loader.render_to_string(
        template,
        {"username": username},
    )

    msg = django.core.mail.EmailMultiAlternatives(
        subject="Activate your account",
        body=html_content,
        from_email=django.conf.settings.EMAIL_HOST,
        to=[email],
    )
    msg.content_subtype = "html"
    msg.send()
