# Generated by Django 4.2.2 on 2023-07-02 09:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_remove_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!", regex='(0|91)?[7-9][0-9]{9}')]),
        ),
    ]
