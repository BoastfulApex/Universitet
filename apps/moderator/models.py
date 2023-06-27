from django.db import models
from users.models import User


ACCOUNTANT, TEACHER, SUPERADMIN = (
    "Buxgalter",
    "O'qituvchi",
    "Admin"
)


class Moderator(User):
    position = models.CharField(max_length=100)
    avatar = models.ImageField(null=True)

    # create_test = models.BooleanField(default=False)
    # create_groups = models.BooleanField(default=False)
    # create_faculty = models.BooleanField(default=False)
