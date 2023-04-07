from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year + 1:
        raise ValidationError(
            ('Год %(value)s больше текущего!'),
            params={'value': value},
        )
