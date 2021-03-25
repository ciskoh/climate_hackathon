from django.core.management.base import BaseCommand
import src.data.retrieve_data
from src.data.retrieve_data import get_gee_data


class Command(BaseCommand):
    help = "manage.py import_data"

    def handle(self, *args, **options):
        get_gee_data()
