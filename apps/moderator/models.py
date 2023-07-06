from django.db import models
from users.models import User


ACCOUNTANT, TEACHER, SUPERADMIN = (
    "Buxgalter",
    "O'qituvchi",
    "Admin"
)


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    position = models.CharField(max_length=100)
    avatar = models.ImageField(null=True)

    create_group_faculty_type = models.BooleanField(default=False)
    create_subject = models.BooleanField(default=False)
    working_with_applicant = models.BooleanField(default=False)
    working_with_student = models.BooleanField(default=False)
    send_message = models.BooleanField(default=False)
    edit_group = models.BooleanField(default=False)
    finance = models.BooleanField(default=False)
