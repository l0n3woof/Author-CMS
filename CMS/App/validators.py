import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def validate_phone_field(value):
    if type(value) != int:
        raise ValidationError("Please enter only digits for phone number.")
    if len(str(value)) != 10:
        raise ValidationError("Phone number field needs to be of 10 digits.")
    return value

def validate_pincode_field(value):
    if type(value) != int:
        raise ValidationError("Please enter only digits for pin-code.")
    if len(str(value)) != 6:
        raise ValidationError("Pin-code needs to be of 6 digits.")
    return value

class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )
    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )

class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )
    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )

