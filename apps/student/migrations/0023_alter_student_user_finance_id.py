# Generated by Django 4.2.2 on 2023-07-29 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_alter_student_user_finance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_finance_id',
            field=models.PositiveIntegerField(default=49646, editable=False, null=True, unique=True),
        ),
    ]
