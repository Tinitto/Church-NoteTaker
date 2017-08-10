from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from user.models import GENDERS
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import same_parent_organization_validator


# This contains models for the program
# Program
# PermittedUserAttributes
# Member - Through to User



PERMISSION_LEVELS = (
    ('N', 'Non-member'),
    ('O', 'Ordinary Member'),
    ('E', 'Editor'),
    ('A', 'Admin'),
)


class Program(models.Model):
    '''
    Each Minute set belongs to a program which in turn belongs to an Organization
    '''
    organization = models.ForeignKey('organization.Organization', related_name='programs',
                                     on_delete=models.CASCADE)
    parent_program = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                                       null=True, related_name='subprograms',
                                       limit_choices_to={'parent_program': None})
    name = models.CharField(max_length=65)
    slug = models.SlugField(max_length=75, unique=True)
    description = models.TextField(max_length=400, blank=True, default='')
    members = models.ManyToManyField(User, related_name='programs_beloged_to', blank=True,
                                     through='Member')


    # override save
    def save(self, *args, **kwargs):
        if not self.id: # i.e. newly saved
            self.slug = slugify(self.organization.name[:5] + ' ' + self.name)
        same_parent_organization_validator(self)
        super(Program, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('organization', 'name'),)


class PermittedUserAttributes(models.Model):
    """
    Program membership limitation by age, location, gender
    """
    program = models.OneToOneField(Program, on_delete=models.CASCADE, related_name='permitteduserattributes')
    min_age = models.IntegerField(verbose_name='minimum age', help_text='minimum age in years',
                                  null=True, blank=True)
    max_age = models.IntegerField(verbose_name='maximum age', help_text='maximum age in years',
                                  null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, default='E')
    countries = models.ManyToManyField('location.Country', blank=True)
    regions = models.ManyToManyField('location.Region', blank=True)
    cities = models.ManyToManyField('location.City', blank=True)
    localareas = models.ManyToManyField('location.LocalArea', blank=True)


@receiver(post_save, sender=Program)
def update_program_user_attributes(sender, instance, created, **kwargs):
    """
    Create an set of permitteduser attributes when a program is created
    """
    if created:
        PermittedUserAttributes.objects.create(program=instance)
    instance.permitteduserattributes.save()



class Member(models.Model):
    '''
    Program members
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='programs')
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=PERMISSION_LEVELS, default='N')
    minutes = models.ManyToManyField('minutes.Minute', through='minutes.Point',
                                    related_name='author', blank=True)

    class Meta:
        unique_together = (('user', 'program'),)
