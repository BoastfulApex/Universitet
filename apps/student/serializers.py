from rest_framework import serializers
from users.models import *
from university.serializers import *
from .models import *


# class RegistrationApplicationSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Application
#         fields = ['id', 'full_name', 'phone', 'passport_seria', 'date_if_birth', 'diploma_picture', 'ielts_picture',
#                   'study_type', 'faculty', 'type']
#


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['id', 'user', 'second_phone', 'passport_seria', 'date_if_birth', 'diploma_picture', 'ielts_picture',
                  'diploma_seria', 'study_type', 'faculty', 'type', 'application_type']


class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['id', 'user', 'second_phone', 'passport_seria', 'date_if_birth', 'diploma_picture', 'ielts_picture',
                  'diploma_seria', 'study_type', 'faculty', 'type', 'acceptance_order', 'course_order', 'removal_order',
                  'academic_certificate', 'university_license', 'university_accreditation', 'application_type']


class TestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['application', 'id', 'guid']


class TestStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'guid']



class StudentAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestQuestion
        fields = ['id', 'student_answer']


