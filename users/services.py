from django.core.cache import cache
from django.core.mail import send_mail

from django_conf import settings

from common.services import generate_random_phrase
from config import OTP_TTL_IN_SEC, OTP_LENGTH


def generate_otp():
    return generate_random_phrase(OTP_LENGTH)


def get_otp_for_email(email: str) -> str:
    email_otp = cache.get(email)
    if email_otp:
        return email_otp

    email_otp = generate_otp()
    cache.set(email, email_otp, timeout=OTP_TTL_IN_SEC)

    return email_otp


def check_otp(email: str, otp: str) -> bool:
    source_otp = cache.get(email)
    if not source_otp:
        return False
    return otp == source_otp


def generate_family_invite_code(family_id, user_id) -> str:
    family_hex = hex(family_id)[2:7]
    user_hex = hex(user_id)[2:7]
    random_chars = generate_random_phrase(6)

    invite_code = family_hex + user_hex + random_chars

    return invite_code
  

def send_otp_email(email, otp):
    subject = 'Код регистрации'
    message = f'Ваш код регистрации: {otp}'
    recipient_list = [email]
    send_mail(subject, message, recipient_list=recipient_list, from_email=settings.EMAIL_HOST)
