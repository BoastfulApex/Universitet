# Generated by Django 4.2.2 on 2023-06-29 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='full_name',
        ),
        migrations.RemoveField(
            model_name='application',
            name='phone',
        ),
    ]
