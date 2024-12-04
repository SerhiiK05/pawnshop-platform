from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string

User = get_user_model()


class EmailService:
    from_email = settings.EMAIL_HOST_USER

    def send_activation_email(
        self, username: str, domain: str, to_email: str, uid: str, token: str
    ) -> None:
        mail_subject = "Activation link has been sent to your email id"

        context = {
            "username": username,
            "domain": domain,
            "uid": uid,
            "token": token,
        }

        message = render_to_string("accounts/activate_email.html", context)
        send_mail(mail_subject, message, self.from_email, [to_email], fail_silently=False)

    def send_message_created(self, user: User, message: str):
        mail_subject = f"New message from user: {user.username}"
        to_email_list = list(
            User.objects.filter(~Q(email=""), email__isnull=False)
            .exclude(id=user.id)
            .values_list("email", flat=True)
        )

        send_mail(mail_subject, message, self.from_email, to_email_list)
