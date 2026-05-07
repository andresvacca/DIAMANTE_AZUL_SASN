from django.core.exceptions import ValidationError
import re


class ClassAuthenticatorPassword:
    def validate(self, password, user=None):
        if not re.findall(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("La contraseña debe contener al menos un carácter especial (ej: !@#$%^&*).",
                code='password_no_symbol',
                )
            
            
        if not re.findall(r'[0-9]', password):
            raise ValidationError("La contraseña debe contener al menos un numero especial (ej: [0-9]).",
                code='password_no_number',
                )
    def get_help_text(self):
        return "Tu contraseña debe incluir al menos un carácter especial y un numero como !@#$%^&* y [0-9]."