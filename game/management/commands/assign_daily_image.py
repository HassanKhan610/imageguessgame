# management/commands/assign_daily_image.py
from django.core.management.base import BaseCommand
from game.views import assign_daily_image

class Command(BaseCommand):
    help = 'Assign a new daily image'

    def handle(self, *args, **kwargs):
        assign_daily_image()