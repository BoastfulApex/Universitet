# Generated by Django 4.2.3 on 2023-07-07 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_application_phone'),
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotFaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lang', models.IntegerField(choices=[(1, "O'zbek"), (2, 'Rus'), (3, 'Ingliz')])),
                ('mode', models.IntegerField(choices=[(1, 'Kunduzgi'), (2, 'Kechgi'), (3, 'Sirtqi')])),
            ],
        ),
        migrations.AddField(
            model_name='botuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='botuser',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.student'),
        ),
    ]
