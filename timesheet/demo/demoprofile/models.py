from django.db import models
from userprofile.models import BaseProfile
from django.utils.translation import ugettext as _
from django.conf import settings
import datetime
from django.contrib.auth.models import User

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

class Profile(BaseProfile):
    firstname = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    birthdate = models.DateField(default=datetime.date.today(), blank=True)
    url = models.URLField(blank=True)
    about = models.TextField(blank=True)

class Chunk(models.Model):
	'a time chunk'
	application = models.CharField(max_length=300, blank=True)
	timestamp = models.DateTimeField()
	person = models.ForeignKey(User)
        
        def __unicode__(self):
            return u"%s: %s, %s" % (self.person.username, self.application, self.timestamp.strftime("%a, %d %b %Y %H:%M:%S"))


