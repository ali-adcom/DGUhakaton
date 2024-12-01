import random
import string


def generate_random_phrase(length: int):
    chars = string.ascii_letters + string.digits
    phrase = ''.join(random.choice(chars) for _ in range(length))
    return phrase
