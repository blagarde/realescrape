from django.core.management.base import BaseCommand
from realescrape.models import Property, Load
from json import load
from codecs import open as copen
from django.db.utils import IntegrityError


def import_items(properties):    
    FIELDS = Property._meta.get_all_field_names()    
    skipped = 0
    load = Load.objects.create()
    for dct in properties:
        kwargs = {k:v for k, v in dct.items() if k in FIELDS}
        kwargs['load'] = load
        try:
            Property.objects.create(**kwargs)
        except IntegrityError:
            skipped += 1
    imported = len(properties) - skipped
    tpl = (imported, skipped)
    if imported == 0:
        load.delete()
    print 'Imported %s properties (skipped %s already existing)' % tpl


class Command(BaseCommand):
    help = 'Import one or more JSON scrape files'

    def add_arguments(self, parser):
        parser.add_argument('json_in', nargs='+', type=str)

    def handle(self, *args, **options):
        for filename in args:
            with copen(filename, 'r', encoding='utf8') as fh:
                self.stdout.write("Processing: %s ..." % filename)
                properties = load(fh)
                import_items(properties)
