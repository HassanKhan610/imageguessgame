# management/commands/run_assign_image.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
import time

class Command(BaseCommand):
    help = 'Runs assign_image command every 5 minutes'

    def handle(self, *args, **kwargs):
        while True:
            call_command('assign_image')
            time.sleep(300)  # Sleep for 5 minutes