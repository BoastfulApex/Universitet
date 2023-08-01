from django.db import models
from telegram import Update, User as TgUser

# Create your models here.


class BotUser(models.Model):
    chat_id = models.BigIntegerField(default=0)
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    number = models.CharField(max_length=255, null=True, blank=True)

    passport = models.CharField(max_length=255, null=True, blank=True)


    pending_test = models.ForeignKey("student.Test", on_delete=models.SET_NULL, null=True, blank=True)


    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True)




    is_verified = models.BooleanField(default=False)
    is_registered = models.BooleanField(default=False)

    @classmethod
    def get(cls, update: Update) -> "tuple[TgUser, BotUser, UserTemp]":
        tgUser = (
            update.message
            or update.callback_query
            or update.pre_checkout_query
            or update.edited_message
            or update.my_chat_member
        ).from_user

        user: "BotUser" = cls.objects.filter(chat_id=tgUser.id).first()
        return tgUser, user, user.temp if user else None

    @property
    def temp(self):
        return UserTemp.objects.filter(user=self).first() or UserTemp.objects.create(
            user=self
        )


class UserTemp(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE)

    utp = models.IntegerField(default=0)

    faculty = models.ForeignKey(
        "university.Faculty", on_delete=models.SET_NULL, null=True, blank=True
    )

    faculty_dir = models.ForeignKey(
        "university.FacultyType", on_delete=models.SET_NULL, null=True, blank=True
    )

    mode = models.IntegerField(
        choices=[
            (0, "Unknown"),
            (1, "Kunduzgi"),
            (2, "Kechgi"),
            (3, "Sirtqi"),
        ],
        default=0,
    )









class BotApplication(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.SET_NULL, null=True, blank=True)

    application = models.ForeignKey('student.Application', on_delete=models.SET_NULL, null=True, blank=True)

    test = models.ForeignKey('student.Test', on_delete=models.SET_NULL, null=True, blank=True)