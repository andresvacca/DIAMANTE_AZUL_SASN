from django.core.exceptions import ValidationError
import re

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # 1. Validación de Caracteres Especiales
        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                "La contraseña debe contener al menos un carácter especial.",
                code='password_no_symbol',
            )

        # 2. Validación de Números (El que quieres agregar)
        if not re.findall(r'[0-9]', password):
            raise ValidationError(
                "La contraseña debe contener al menos un número.",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Tu contraseña debe incluir al menos un número y un carácter especial (!@#$)."