from django.core.exceptions import ValidationError
import os


def validate_academic_year_format(value):
    if not value or len(value) != 9 or not value[:4].isdigit() or value[4] != '/' or not value[5:].isdigit():
        raise ValidationError('Veuillez saisir l\'année académique dans le format AAAA/AAAA')
    
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only SVG files are allowed.')
