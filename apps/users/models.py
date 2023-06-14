from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random
import requests


def send_sms(otp, phone):
    username = 'onlineqabul'
    password = 'p7LnIrh+-Vw'
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003",
                      "sms": {
                          "originator": "3700",
                          "content": {
                              "text": f"Toshkentiqt isodiyot va pedagodika instituti. Tasdiqlash kodi : {otp}"}
                      }
                      }]
    }
    url = "http://91.204.239.44/broker-api/send"
    res = requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


NEW, FULL, CONFIRMED, CANCELED, REGISTRATION, TRANSFER = (
    "Ariza topshirilmagan",
    "Ko'rib chiqilmoqda",
    "Tasdiqlandi",
    "Rad etildi",
    "Ro'yxatdan o'tish",
    "O'qishni ko'chirish"
)


class User(AbstractUser):
    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )

    full_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    username = None

    phone = models.CharField(max_length=15, null=True, unique=True, validators=[_validate_phone])
    telegram_id = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return "{}".format(self.phone)

    def generate_otp(self):
        otp = random.randint(111111, 999999)
        self.set_password(str(otp))
        self.otp = otp
        self.save()
        send_sms(otp=otp, phone=self.phone)
        return otp


class Application(models.Model):
    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )

    STATUS_TYPES = (
        (FULL, FULL),
        (CONFIRMED, CONFIRMED),
        (CANCELED, CANCELED)
    )

    APPLICATION_TYPES = (
        (REGISTRATION, REGISTRATION),
        (TRANSFER, TRANSFER)
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    second_phone = models.CharField(max_length=15, null=True, validators=[_validate_phone])

    study_type = models.ForeignKey('university.StudyType', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('university.FacultyType', on_delete=models.SET_NULL, null=True)

    passport_seria = models.CharField(_("Passport Seriyasi"), max_length=150, blank=True, null=True)
    date_if_birth = models.DateField(null=True, blank=True)
    diploma_seria = models.CharField(_("Diplom Seriyasi"), max_length=150, blank=True, null=True)
    diploma_picture = models.ImageField(null=True)

    ielts_picture = models.ImageField(null=True)

    acceptance_order = models.ImageField(null=True)
    course_order = models.ImageField(null=True)
    removal_order = models.ImageField(null=True)
    academic_certificate = models.ImageField(null=True)
    university_license = models.ImageField(null=True)
    university_accreditation = models.ImageField(null=True)

    application_type = models.CharField(max_length=100, choices=APPLICATION_TYPES)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS_TYPES, default=FULL)
