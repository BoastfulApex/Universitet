# Generated by Django 4.2.2 on 2023-07-06 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0015_alter_group_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facultytype',
            old_name='description_file',
            new_name='malumotnoma_file',
        ),
        migrations.AddField(
            model_name='facultytype',
            name='shartnoma_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]