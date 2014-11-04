from django.db.models import Model, CharField, DateTimeField, FloatField, TextField, BooleanField, IntegerField, ForeignKey
from django.core.serializers import serialize
from django.conf import settings
from codecs import open as copen
from unidecode import unidecode
import re


BLACKLIST = [re.compile(unidecode(l.rstrip('\n').lower())) for l in copen(settings.BLACKLIST_FILENAME, 'r', encoding='utf8')]


class Load(Model):
    timestamp = DateTimeField(auto_now=True)


class Property(Model):
    url = CharField(max_length=200, unique=True)
    price = FloatField()
    size = FloatField()
    description = TextField()
    title = TextField()
    postcode = IntegerField()
    load = ForeignKey(Load)
    
    updated = DateTimeField(auto_now=True)
    phone = CharField(max_length=15)
    listed_on = CharField(max_length=15)

    unread = BooleanField(default=True)
    blacklisted = DateTimeField(null=True, blank=True)
    star = BooleanField(default=False)
    notes = TextField(default="")

    @property
    def ppsqm(self):
        return self.price / self.size

    @property
    def display(self):
        contents = unidecode(self.title.lower()) + unidecode(self.description.lower()).replace('\n', ' ')
        return not any([regex.search(contents) is not None for regex in BLACKLIST]) and not self.blacklisted

    def as_dict(self, fields="url price description title postcode star size ppsqm unread notes".split(' ')):
        return {f:getattr(self, f) for f in fields}

    def __unicode__(self):
        return u"%s (%s sqm, %s EUR/sqm)" % (self.title, self.size, self.ppsqm)