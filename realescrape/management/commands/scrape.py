from django.core.management.base import BaseCommand
from realescrape.scraper import Scraper


class Command(BaseCommand):
    help = 'Scrape and populate the database'

    def handle(self, *args, **options):
        Scraper()
