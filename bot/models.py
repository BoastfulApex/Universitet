from typing import TYPE_CHECKING
from django.db import models
from telegram import (
    Update,
    User as TgUser
)

if TYPE_CHECKING:
    from apps.university.models import Question

from utils import distribute

# Create your models here.





class BotUser(models.Model):
    chat_id = models.BigIntegerField()
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    otp = models.IntegerField(default=0)


    student = models.ForeignKey("student.Student",on_delete=models.SET_NULL,null=True)
    is_verified = models.BooleanField(default=False)



    
    @classmethod
    def get(cls,update:Update) -> "tuple[TgUser, BotUser]":
        tgUser = (update.message or update.callback_query or update.pre_checkout_query).from_user
        user: BotUser = cls.objects.filter(chat_id=tgUser.id).first()
        return tgUser,user
    






class BotFaculty(models.Model):
    name = models.CharField(max_length=255)
    lang = models.IntegerField(choices=[
        (1,"O'zbek"),
        (2,"Rus"),
        (3,"Ingliz"),
    ])

    mode = models.IntegerField(choices=[
        (1,"Kunduzgi"),
        (2,"Kechgi"),
        (3,"Sirtqi"),
    ])


    @classmethod
    def keyboard(self,lang,mode):
        return distribute([fac.name for fac in self.objects.filter(lang=lang,mode=mode)],2)




class TestSession(models.Model):
    user = models.ForeignKey(BotUser,on_delete=models.CASCADE)
    questions = models.ManyToManyField('university.Question')
    current_question: "Question" = models.ForeignKey('university.Question',on_delete=models.SET_NULL,null=True,blank=True,related_name="Current_Question")

    trueAnswersCount = models.IntegerField(default=0)
    questionCount = models.IntegerField(default=1)
    questionIndex = models.IntegerField(default=1)
    ball = models.IntegerField(default=0)

    is_passed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    @property
    def question(self) -> "Question":
        question = self.questions.order_by("?").first()
        self.current_question = question
        self.questions.remove(question)
        self.save()
        return question