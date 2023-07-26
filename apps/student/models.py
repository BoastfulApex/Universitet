import uuid
from django.db import models
from users.models import User
from university.models import Question, get_random_choice
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
import random


NEW, FULL, CONFIRMED, CANCELED, REGISTRATION, TRANSFER, CONSULTATION = (
    "Ariza topshirilmagan",
    "Ko'rib chiqilmoqda",
    "Tasdiqlandi",
    "Rad etildi",
    "Ro'yxatdan o'tish",
    "O'qishni ko'chirish",
    "Konsultatsiya"
)


kurs1, kurs2, kurs3, kurs4 = (
    "1-Kurs",
    "2-Kurs",
    "3-Kurs",
    "4-Kurs",
)


class Student(models.Model):
    KURS = (
        (kurs1, kurs1),
        (kurs2, kurs2),
        (kurs3, kurs3)
    )

    _validate_phone = RegexValidator(
        regex="(0|91)?[7-9][0-9]{9}",
        message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_finance_id = models.PositiveIntegerField(
        default=random.randint(10000, 99999),
        unique=True,
        null=True,
        editable=False,
    )
    group = models.ForeignKey('university.Group', on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True, null=True)

    second_phone = models.CharField(max_length=15, null=True, validators=[_validate_phone])

    study_type = models.ForeignKey('university.StudyType', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('university.FacultyType', on_delete=models.SET_NULL, null=True)

    passport_seria = models.CharField(_("Passport Seriyasi"), max_length=150, blank=True, null=True)
    date_if_birth = models.DateField(null=True, blank=True)
    diploma_seria = models.CharField(_("Diplom Seriyasi"), max_length=150, blank=True, null=True)
    diploma_picture = models.ImageField(null=True, blank=True)

    ielts_picture = models.ImageField(null=True, blank=True)

    acceptance_order = models.ImageField(null=True, blank=True)
    course_order = models.ImageField(null=True, blank=True)
    removal_order = models.ImageField(null=True, blank=True)
    academic_certificate = models.ImageField(null=True, blank=True)
    university_license = models.ImageField(null=True, blank=True)
    university_accreditation = models.ImageField(null=True, blank=True)
    course = models.CharField(max_length=100, null=True, choices=KURS)

    contract_amount1 = models.IntegerField(default=0)
    contract_amount2 = models.IntegerField(default=0)

    first_quarter = models.DateField(null=True)
    second_quarter = models.DateField(null=True)

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.full_name = self.user.full_name
    #     super(Student, self).save(*args, **kwargs)


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
        (TRANSFER, TRANSFER),
        (CONSULTATION, CONSULTATION)
    )

    KURS = (
        (kurs1, kurs1),
        (kurs2, kurs2),
        (kurs3, kurs3),
        (kurs4, kurs4)
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(_("full name"), max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, validators=[_validate_phone])

    second_phone = models.CharField(max_length=15, null=True, validators=[_validate_phone])

    study_type = models.ForeignKey('university.StudyType', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey('university.Faculty', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('university.FacultyType', on_delete=models.SET_NULL, null=True)

    passport_seria = models.CharField(_("Passport Seriyasi"), max_length=150, blank=True, null=True)
    date_if_birth = models.DateField(null=True, blank=True)
    diploma_seria = models.CharField(_("Diplom Seriyasi"), max_length=150, blank=True, null=True)
    diploma_picture = models.ImageField(null=True, blank=True)

    ielts_picture = models.ImageField(null=True, blank=True)
    kurs_for = models.CharField(max_length=100, null=True, choices=KURS)

    acceptance_order = models.ImageField(null=True, blank=True)
    course_order = models.ImageField(null=True, blank=True)
    removal_order = models.ImageField(null=True, blank=True)
    academic_certificate = models.ImageField(null=True, blank=True)
    university_license = models.ImageField(null=True, blank=True)
    university_accreditation = models.ImageField(null=True, blank=True)

    application_type = models.CharField(max_length=100, choices=APPLICATION_TYPES, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS_TYPES, default=FULL)

    is_privilege = models.BooleanField(default=False)
    test_passed = models.BooleanField(default=False)

    description = models.CharField(max_length=10000, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.type:
            self.is_privilege = self.type.check_privilege()
        if not self.pk:
            self.phone = self.user.phone
        super(Application, self).save(*args, **kwargs)


class Test(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField(null=True, blank=True)
    finish_date = models.DateTimeField(null=True, blank=True)


class TestQuestion(models.Model):
    subject = models.ForeignKey('student.TestSubject', on_delete=models.CASCADE)
    question = models.ForeignKey('university.Question', on_delete=models.CASCADE)
    student_answer = models.ForeignKey('university.Answer', on_delete=models.CASCADE, null=True, blank=True)
    solved = models.BooleanField(default=False)


class TestSubject(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    subject = models.ForeignKey('university.Subject', on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    ball = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class StudentFinance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    summa = models.PositiveIntegerField()


class Agreement(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    agreement_file = models.FileField(null=True, upload_to='./agreements/')
    file_path = models.CharField(null=True, max_length=2000)

