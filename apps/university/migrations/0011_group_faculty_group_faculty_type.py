# Generated by Django 4.2.2 on 2023-06-28 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0010_remove_group_faculty_remove_group_faculty_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='university.faculty'),
        ),
        migrations.AddField(
            model_name='group',
            name='faculty_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='university.facultytype'),
        ),
    ]
