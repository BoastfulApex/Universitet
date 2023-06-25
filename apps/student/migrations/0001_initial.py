# Generated by Django 4.2.2 on 2023-06-25 06:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('university', '0007_alter_subject_one_question_ball'),
        ('users', '0010_delete_application'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=100, null=True)),
                ('second_phone', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!", regex='(0|91)?[7-9][0-9]{9}')])),
                ('passport_seria', models.CharField(blank=True, max_length=150, null=True, verbose_name='Passport Seriyasi')),
                ('date_if_birth', models.DateField(blank=True, null=True)),
                ('diploma_seria', models.CharField(blank=True, max_length=150, null=True, verbose_name='Diplom Seriyasi')),
                ('diploma_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('ielts_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('acceptance_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('course_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('removal_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('academic_certificate', models.ImageField(blank=True, null=True, upload_to='')),
                ('university_license', models.ImageField(blank=True, null=True, upload_to='')),
                ('university_accreditation', models.ImageField(blank=True, null=True, upload_to='')),
                ('application_type', models.CharField(blank=True, choices=[("Ro'yxatdan o'tish", "Ro'yxatdan o'tish"), ("O'qishni ko'chirish", "O'qishni ko'chirish"), ('Konsultatsiya', 'Konsultatsiya')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[("Ko'rib chiqilmoqda", "Ko'rib chiqilmoqda"), ('Tasdiqlandi', 'Tasdiqlandi'), ('Rad etildi', 'Rad etildi')], default="Ko'rib chiqilmoqda", max_length=50, null=True)),
                ('is_privilege', models.BooleanField(default=False)),
                ('test_passed', models.BooleanField(default=False)),
                ('description', models.CharField(blank=True, max_length=10000, null=True)),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.faculty')),
                ('study_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.studytype')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.facultytype')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('finish_date', models.DateTimeField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.application')),
            ],
        ),
        migrations.CreateModel(
            name='TestSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answers', models.IntegerField(default=0)),
                ('wrong_answers', models.IntegerField(default=0)),
                ('ball', models.FloatField(default=0)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.subject')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.test')),
            ],
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solved', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='university.question')),
                ('student_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='university.answer')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.testsubject')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('second_phone', models.CharField(max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Telefon raqam Xalqaro Formatda 998YYXXXXXXX ko'rinishida kiritilishi kerak!", regex='(0|91)?[7-9][0-9]{9}')])),
                ('passport_seria', models.CharField(blank=True, max_length=150, null=True, verbose_name='Passport Seriyasi')),
                ('date_if_birth', models.DateField(blank=True, null=True)),
                ('diploma_seria', models.CharField(blank=True, max_length=150, null=True, verbose_name='Diplom Seriyasi')),
                ('diploma_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('ielts_picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('acceptance_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('course_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('removal_order', models.ImageField(blank=True, null=True, upload_to='')),
                ('academic_certificate', models.ImageField(blank=True, null=True, upload_to='')),
                ('university_license', models.ImageField(blank=True, null=True, upload_to='')),
                ('university_accreditation', models.ImageField(blank=True, null=True, upload_to='')),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.faculty')),
                ('study_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.studytype')),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='university.facultytype')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('users.user',),
        ),
    ]
