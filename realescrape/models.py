from django.db.models import Model, CharField, DateTimeField, FloatField, TextField, BooleanField, IntegerField
from django.core.serializers import serialize
from django.conf import settings
from codecs import open as copen
from unidecode import unidecode
import re


BLACKLIST = [re.compile(unidecode(l.rstrip('\n').lower())) for l in copen(settings.BLACKLIST_FILENAME, 'r', encoding='utf8')]


class Property(Model):
    url = CharField(max_length=200, unique=True)
    price = FloatField()
    description = TextField()
    title = TextField()
    postcode = IntegerField()
    
    updated = DateTimeField(auto_now=True)
    size = FloatField()
    phone = CharField(max_length=15)
    listed_on = CharField(max_length=15)

    unread = BooleanField(default=True)
    blacklisted = DateTimeField(auto_now=True, null=True)
    star = BooleanField(default=False)

    @property
    def ppsqm(self):
        return self.price / self.size

    @property
    def display(self):
        contents = unidecode(self.title.lower()) + unidecode(self.description.lower())
        return not any([regex.search(contents) is not None for regex in BLACKLIST])

    def __unicode__(self):
        return u"%s (%s sqm, %s EUR/sqm)" % (self.title, self.size, self.ppsqm)