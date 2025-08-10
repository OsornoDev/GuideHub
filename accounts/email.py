from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
import os
import logging

logger = logging.getLogger(__name__)

def send_mail_django(to_email: str, subject: str, template_name: str, data: dict) -> bool:
    """Enviar correo con plantilla HTML e imagen embebida usando Django."""
    try:
        # Renderizar plantilla HTML desde templates/
        html_content = render_to_string(f"{template_name}.html", data)

        # Crear correo
        email = EmailMultiAlternatives(
            subject=subject,
            body="Este es un mensaje HTML. Por favor usa un cliente que soporte HTML.",
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")

        # Adjuntar logo si existe
        logo_path = os.path.join(settings.BASE_DIR, "static/img/logo.svg")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as img:
                logo = MIMEImage(img.read())
                logo.add_header("Content-ID", "<logo>")
                logo.add_header("Content-Disposition", "inline", filename="logo.svg")
                email.attach(logo)

        email.send()
        logger.info(f"Correo enviado exitosamente a {to_email}")
        return True

    except Exception as e:
        logger.error(f"Error enviando correo: {str(e)}", exc_info=True)
        return False
