import os
from django.core.management.base import BaseCommand

from tg_bot import Bot




class Command(BaseCommand):


    def handle(self,*args,**kwargs):
        token = os.getenv("TOKEN")

        bot = Bot(token)

        bot.app.run_polling()