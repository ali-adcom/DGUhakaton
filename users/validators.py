from django.core.exceptions import ValidationError


def validate_age(age):
    if age <= 0 or age >= 150:
        raise ValidationError(
            f'Возраст {age} не является допустимым. Возраст должен быть в диапазоне от 0 до 150 лет.'
        )
