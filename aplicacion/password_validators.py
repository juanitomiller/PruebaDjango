# aplicacion/password_validators.py

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Tu contraseña debe contener al menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Tu contraseña debe contener al menos %(min_length)d caracteres."
        ) % {'min_length': self.min_length}

class CustomCommonPasswordValidator:
    def validate(self, password, user=None):
        common_passwords = ['123456', 'password', '12345678']
        if password in common_passwords:
            raise ValidationError(
                _("Tu contraseña no puede ser una clave utilizada comúnmente."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Tu contraseña no puede ser una clave utilizada comúnmente.")

class CustomNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Tu contraseña no puede ser completamente numérica."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Tu contraseña no puede ser completamente numérica.")

class CustomUserAttributeSimilarityValidator:
    def __init__(self, user_attributes=None, max_similarity=0.7):
        if user_attributes is None:
            user_attributes = ['username', 'first_name', 'last_name', 'email']
        self.user_attributes = user_attributes
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        for attribute_name in self.user_attributes:
            value = getattr(user, attribute_name, None)
            if not value or not isinstance(value, str):
                continue
            value_parts = value.split()
            for value_part in value_parts:
                if value_part.lower() in password.lower():
                    similarity = len(value_part) / len(password)
                    if similarity > self.max_similarity:
                        raise ValidationError(
                            _("Tu contraseña no puede asemejarse tanto a tu %(verbose_name)s."),
                            code='password_too_similar',
                            params={'verbose_name': attribute_name},
                        )

    def get_help_text(self):
        return _("Tu contraseña no puede asemejarse tanto a tu otra información personal.")
