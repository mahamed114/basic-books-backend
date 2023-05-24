from django.core.mail import send_mail
from django.conf import settings
import random


from .models import User


def send_otp_via_email(email):
    subject = "Basic Books Account Verification"
    otp = random.randint(1000, 9999)
    message = f"Your OTP Code is {otp}"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()


def send_invite_via_email(email, name, orgname):
    subject = f"{orgname} sent you an invite"
    message = f"Hi {name} {orgname} is inviting you to manage their Basic Books account as employee. \nuse this email {email} to signin at https://books.basicbooks.com/signin"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])
