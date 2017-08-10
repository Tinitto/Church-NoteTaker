from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from user.models import GENDERS
from django.db.models.signals import post_save
from django.dispatch import receiver


# This contains the follwoing models
# Category
# Organization
# Admin - Through to User from Organization
# Branch - Through to location.LocalArea


class Category(models.Model):
    """
    Each organization falls in one category
    """
    name = models.CharField(max_length=65, unique=True)
    slug = models.SlugField(max_length=65)

    # override save
    def save(self, *args, **kwargs):
        if not self.id:   # i.e. newly saved
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Organization(models.Model):
    """
    Each Program is under a given organization. Each organization is associated to one creator - user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_organizations')
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=75, unique=True)
    emblem = models.ImageField(upload_to='organization/emblem', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='organizations',
                                 null=True, blank=True)
    #branches = models.ManyToManyField('location.LocalArea', through='Branch', blank=True)
    admins = models.ManyToManyField(User, blank=True, related_name='administered_organizations')
    approved = models.BooleanField(default=False) # an organization will only be active after
    # the superadmin has approved it

    def save(self, *args, **kwargs):
        if not self.id or not self.slug: # i.e. newly saved
            self.slug = slugify(self.name)
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Branch(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='branches')
    name = models.CharField(max_length=65, default='', blank=True)
    localarea = models.ForeignKey('location.LocalArea', on_delete=models.SET_NULL,
                                  null=True, related_name='branch')

    class Meta:
        unique_together = ('organization', 'name')