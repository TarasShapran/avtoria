from django.core.exceptions import ValidationError


class ProfanityValidationError(ValidationError):
    pass