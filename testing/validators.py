from django.core.exceptions import ValidationError


def validate_academic_year_format(value):
    if not value or len(value) != 9 or not value[:4].isdigit() or value[4] != '/' or not value[5:].isdigit():
        raise ValidationError('Veuillez saisir l\'année académique dans le format AAAA/AAAA')
