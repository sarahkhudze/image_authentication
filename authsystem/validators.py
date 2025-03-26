# authsystem/validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class SpecialCharacterValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Password must contain at least one letter."),
                code='password_no_letter',
            )
        if not any(char in '!@#$%^&*()_+-=[]{};:,.<>?/' for char in password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )

    def get_help_text(self):
        return _(
            "Your password must contain:"
            "\n- At least 8 characters"
            "\n- At least one letter"
            "\n- At least one number"
            "\n- At least one special character (!@#$%^&* etc.)"
        )