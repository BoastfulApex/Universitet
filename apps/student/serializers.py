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
        fields = "__all__"


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

    # def validate(self, attrs):
    #     # Perform your validation logic here
    #     # You can access the validated data using `attrs`
    #
    #     # Example validation: Check if application is active
    #     application = attrs.get('application')
    #     test = Test.objects.filter(application_id=application).first()
    #     if test:
    #         raise serializers.ValidationError(f"{test.guid}")
    #     return attrs


class TestStartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['id', 'guid']


class StudentAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestQuestion
        fields = ['id', 'student_answer']


