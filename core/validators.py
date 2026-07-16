from django.core.exceptions import ValidationError

def validate_file_size(value):
    """
    Validates that the uploaded file does not exceed 5 MB.
    """
    limit_mb = 5
    limit = limit_mb * 1024 * 1024
    if value.size > limit:
        raise ValidationError(f'File size cannot exceed {limit_mb} MB.')
