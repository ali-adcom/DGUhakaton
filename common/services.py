from datetime import datetime
import random
import string

from django.db.models import Q



def generate_random_phrase(length: int):
    chars = string.ascii_letters + string.digits
    phrase = ''.join(random.choice(chars) for _ in range(length))
    return phrase

def get_tasks_month_filter(year: int, month: int) -> Q:
    start_date = datetime(year, month, day=1)
    
    DECEMBER = 12
    JANUARY = 1
    
    if month == DECEMBER:
        end_date = datetime(year=year + 1, month=JANUARY, day=1)
    else:
        end_date = datetime(year, month + 1, 1)

    
    return Q(tasks__created_datetime__gte=start_date) & Q(tasks__created_datetime__lt=end_date)
