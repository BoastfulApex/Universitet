# Generated by Django 4.2.2 on 2023-07-11 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0017_facultytype_first_quarter_facultytype_second_quarter'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facultytype',
            old_name='contract_amount',
            new_name='contract_amount1',
        ),
        migrations.AddField(
            model_name='facultytype',
            name='contract_amount2',
            field=models.IntegerField(default=0),
        ),
    ]
