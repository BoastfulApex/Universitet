# Generated by Django 4.2.2 on 2023-07-06 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_alter_student_user_finance_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='user_finance_id',
        ),
    ]
