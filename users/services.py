from django.core.cache import cache
import random
import string
from config import OTP_TTL_IN_SEC, OTP_LENGTH


def generate_otp():
    chars = string.ascii_letters + string.digits
    otp = ''.join(random.choice(chars) for _ in range(OTP_LENGTH))
    return otp


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
