from django.contrib import admin

# Register your models here.
from .models import BotUser, BotApplication


admin.site.register(BotUser)

admin.site.register(BotApplication)