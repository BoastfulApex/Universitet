# Generated by Django 4.2.2 on 2023-07-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_student_user_finance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_finance_id',
            field=models.PositiveIntegerField(default=44631, editable=False, null=True, unique=True),
        ),
    ]