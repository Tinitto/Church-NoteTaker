from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
#from django.conf import settings
#from rest_framework.authtoken.models import Token

from .validators import PhoneRegex, past_dates_only

# This describes the custom User models
# This includes the following models
# Profile
# Address

GENDERS = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('E', 'Either')
)


class Profile(models.Model):
    """
    One Profile per user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='users/profile', blank=True,
                                      null=True)
    telephone = models.CharField(validators=[PhoneRegex], blank=True,
                                 default='', max_length=20)
    birthday = models.DateField(validators=[past_dates_only], null=True, blank=True)
    gender = models.CharField(choices=GENDERS, default='M', max_length=1)
    email_confirmed = models.BooleanField(default=False)
    localarea = models.ForeignKey('location.LocalArea', on_delete=models.SET_NULL,
                                  null=True, blank=True, related_name='user')


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile when a user is created
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
#    """
#    To automatically create tokens for the user as soon as the user is created
#    """
#    if created:
#        Token.objects.create(user=instance)



#class Address(models.Model):
 #   """
 #   A User's address
 #   """
 #   profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='address')
 #   localarea = models.ForeignKey('location.LocalArea', on_delete=models.SET_NULL,
 #                                 null=True, blank=True)
