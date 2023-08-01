from os import getenv
from typing import Any, Optional
from django.core.management.base import BaseCommand
from tg_bot import Bot














class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        token = getenv('TG_TOKEN')



        bot = Bot(token)

        bot.app.run_polling()