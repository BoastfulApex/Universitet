from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import random


FULL, CONFIRMED, CANCELED = (
    "Ko'rib chiqilmoqda",
    "Tasdiqlandi",
    "Rad etildi"
)


class User(AbstractUser):
    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )

    STATUS_TYPES = (
        (FULL, FULL),
        (CONFIRMED, CONFIRMED),
        (CANCELED, CANCELED)
    )

    full_name = models.CharField(_("first name"), max_length=150, blank=True, null=True)
    email = models.EmailField(_("email address"), blank=True, null=True)
    username = None

    phone = models.CharField(max_length=15, null=True, unique=True, validators=[_validate_phone])
    telegram_id = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=10, null=True, blank=True)

    passport_seria = models.CharField(_("Passport Seriyasi"), max_length=150, blank=True, null=True)
    date_if_birth = models.DateField(null=True, blank=True)
    diploma_seria = models.CharField(_("Diplom Seriyasi"), max_length=150, blank=True, null=True)
    diploma_picture = models.ImageField(null=True)
    ielts_picture = models.ImageField(null=True)

    study_type = models.ForeignKey('university.StudyType', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('university.FacultyType', on_delete=models.SET_NULL, null=True)

    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS_TYPES)

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
        return otp

    def save(self, *args, **kwargs):
        if not self.pk:
            self.status = FULL
        super(User, self).save(*args, **kwargs)
