# Generated by Django 4.2.2 on 2023-07-24 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_create_group_faculty_type_user_create_subject_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='analytica',
            field=models.BooleanField(default=False),
        ),
    ]
