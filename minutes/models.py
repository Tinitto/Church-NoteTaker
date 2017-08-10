from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# This includes the following models
# Agenda
# Minute
# Point
# Author - Through to User from Point

PRIVACY_OPTIONS = (
    (0, 'Public'),
    (1, 'Organization Members'),
    (2, 'Parent Program Members'),
    (3, 'Program Members')
)

SOURCE_TYPES = (
    ('BI', 'Bible'),
    ('BO', 'Other Book'),
    ('WE', 'Website')
)

POINT_TYPES = (
    ('GC', 'General Consensus'),
    ('HM', 'Honorary Mention'),
    ('AOB', 'Any Other Business')
)



class Reference(models.Model):
    source_type = models.CharField(max_length=2, choices=SOURCE_TYPES, default='BI')
    book = models.CharField(max_length=255, default='', blank=True)
    chapter = models.IntegerField(null=True, blank=True)
    verse = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)


class Agenda(models.Model):
    # ensure this is an editor role
    author = models.ForeignKey('program.Member', on_delete=models.SET_NULL, null=True,
                               related_name='agendas')
    privacy = models.IntegerField(choices=PRIVACY_OPTIONS, default=0)#public
    purpose = models.CharField(max_length=65)
    date = models.DateField(auto_now_add=True)
    venue = models.CharField(max_length=256, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.purpose

    class Meta:
        unique_together = (('author', 'purpose', 'date'),)


class Minute(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE,
                               related_name='minutes')
    title = models.CharField(max_length=255)
    references = models.ManyToManyField(Reference,
                                   blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('agenda', 'title'),)


@receiver(post_save, sender=Minute)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Save the parent agenda of a minute whenever a new minute is created
    or updated so as to update the last_modified of the former
    """
    instance.agenda.save()


class Point(models.Model):
    minute = models.ForeignKey(Minute, on_delete=models.CASCADE, related_name='points')
    # need validation or permission to ensure only member belonging to minute's
    # agenda's author's program
    author = models.ForeignKey('program.Member', on_delete=models.CASCADE,
                               related_name='points')
    text_detail = models.CharField(default='', blank=True, max_length=140,
                              help_text='Feed in not more than 140 characters')
    privacy = models.IntegerField(choices=PRIVACY_OPTIONS, default=0)  # public
    point_type = models.CharField(max_length=3, choices=POINT_TYPES, default='GC')
    references = models.ManyToManyField(Reference, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('author', 'minute', 'text_detail'),)


