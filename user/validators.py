from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import ugettext as _
from django.utils import datetime_safe

PhoneRegex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                            message="Phone number must be entered in the format: \
                            '+999999999'. Up to 15 digits allowed.")


def past_dates_only(date_value):
    if date_value > datetime_safe.datetime.now().date():
        raise ValidationError(_('Date should be in the past'))
