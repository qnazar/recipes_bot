from django.core.management.base import BaseCommand

from .handlers import bot


class Command(BaseCommand):
    help = 'Bot'

    def handle(self, *args, **options):
        bot.infinity_polling()
