import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that pauses execution until DB becomes available"""

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.NOTICE('Waiting for database...'))
        db_connection = None
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write(
                    self.style.WARNING('DB unavailable, pausing 1 sec'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DB is available!'))
