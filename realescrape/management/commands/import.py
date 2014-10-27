from django.core.management.base import BaseCommand
from realescrape.models import Property
from json import load
from codecs import open as copen


class Command(BaseCommand):
    help = 'Import one or more JSON scrape files'

    def add_arguments(self, parser):
        parser.add_argument('json_in', nargs='+', type=str)

    def handle(self, *args, **options):
        FIELDS = Property._meta.get_all_field_names()
        for filename in args:
            with copen(filename, 'r', encoding='utf8') as fh:
                properties = load(fh)
                for dct in properties:
                    kwargs = {k:v for k, v in dct.items() if k in FIELDS}
                    Property.objects.create(**kwargs)
            self.stdout.write('Imported %s properties' % len(properties))