from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import ugettext as _
from django.utils import datetime_safe


def same_parent_organization_validator(program):
    if program.parent_program:
        if not program.parent_program.organization == program.organization:
            raise ValidationError(_('Parent program has a different Parent Organization'))
