# Generated by Django 4.2.2 on 2023-07-06 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_alter_student_user_finance_id_studentfinance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user_finance_id',
            field=models.PositiveIntegerField(default=88704, editable=False, null=True, unique=True),
        ),
    ]
