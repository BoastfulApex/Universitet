# Generated by Django 4.2.2 on 2023-07-02 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0011_group_faculty_group_faculty_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='facultytype',
            name='contract_amount',
            field=models.IntegerField(default=0),
        ),
    ]
