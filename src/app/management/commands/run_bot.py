from django.core.management.base import BaseCommand
from app.internal.bot import setup_bot


class Command(BaseCommand):
    help = 'Telegram for_bot'

    def handle(self, *args, **options):
        setup_bot()
