# Generated by Django 4.2.2 on 2023-07-31 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0026_alter_student_user_finance_id'),
        ('bot', '0003_remove_botuser_utp_usertemp'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='pending_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.test'),
        ),
        migrations.CreateModel(
            name='BotApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.application')),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.test')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.botuser')),
            ],
        ),
    ]
