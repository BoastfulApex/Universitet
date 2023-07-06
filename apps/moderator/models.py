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
