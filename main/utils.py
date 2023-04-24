from typing import Dict, Any, List, Optional

from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def render_template_mail(template: str,) -> str:
    message = render_to_string(template)
    return message


def send_mail(
    subject: str,
    message: str,
    recipient: str,
    fail_silently: bool = False,
    attachments: List[Optional[File]] = [],
) -> Any:
    headers: Dict[Any, Any] = {}

    msg = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=settings.FROM_USER,
        to=[recipient,],
        headers=headers,
    )
    msg.attach_alternative(message, "text/html")
    print(attachments)
    for attachment in attachments:
        msg.attach_alternative(content=attachment.file.read(), mimetype="application/vnd.openxmlformats-officedocument" ".spreadsheetml.sheet")
    return msg.send(fail_silently)


def send_template_mail(
    subject: str,
    template: str,
    context: Dict[Any, Any],
    recipient: str,
    fail_silently: bool = False,
) -> Any:
    message = render_template_mail(template)
    return send_mail(subject, message, recipient, fail_silently, attachments=context.get("docs"))
