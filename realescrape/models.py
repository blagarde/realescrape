from django.db.models import Model, CharField, DateTimeField, FloatField, TextField, BooleanField, IntegerField


class Property(Model):
    url = CharField(max_length=200, unique=True)
    price = FloatField()
    description = TextField()
    title = TextField()
    postcode = IntegerField()
    
    updated = DateTimeField(auto_now=True)
    size = FloatField()
    phone = CharField(max_length=15)

    unread = BooleanField(default=True)
    blacklisted = BooleanField(default=False)
    star = BooleanField(default=False)

    @property
    def ppsqm(self):
        return self.fields['price'] / self.fields['size']
