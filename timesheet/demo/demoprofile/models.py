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

PRODUCTIVITY =  (
           (-1, 'unproductive'),
           (0, 'neutral'),
           (1, 'productive'),
)

class Chunk(models.Model):
	'a time chunk'
	application = models.CharField(max_length=300, blank=True)
	timestamp = models.DateTimeField()
	person = models.ForeignKey(User)
        score = models.IntegerField(choices=PRODUCTIVITY, blank=True)
        
        def __unicode__(self):
            return u"%s: %s, %s, score:%d" % (self.person.username, self.application, self.timestamp.strftime("%a, %d %b %Y %H:%M:%S"), self.score)


class Preferences(models.Model):
    'productivity preferences for various applications'
    application = models.CharField(max_length=300, primary_key=True)
    score = models.IntegerField(choices=PRODUCTIVITY)
    person = models.ForeignKey(User, null=True)

    def productivity(self):
        return [x[1] for x in PRODUCTIVITY if x[0]==self.score][0]

    def __unicode__(self):
        score = self.productivity()
        return u"%s: %s, score: %s" % (self.person.username, self.application, score)
