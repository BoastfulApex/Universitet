# Generated by Django 4.2.2 on 2023-07-18 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_alter_student_user_finance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_finance_id',
            field=models.PositiveIntegerField(default=87200, editable=False, null=True, unique=True),
        ),
    ]