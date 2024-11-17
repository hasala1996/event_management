import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Wait for the database to be available"

    def handle(self, *args, **options):
        self.stdout.write("Waitint for the database to be available...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database not available, waiting 1 second...")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("!Database available!"))
