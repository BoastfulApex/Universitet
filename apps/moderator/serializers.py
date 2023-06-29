from rest_framework import serializers
from university.serializers import *
from users.serializers import *
from student.serializers import *
from university.models import Group


class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone', 'full_name', 'otp']


class ApplicationSerializer(serializers.ModelSerializer):
    user = StudentUserSerializer

    class Meta:
        model = Application
        fields = '__all__'


class ApplicationUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    status = serializers.ChoiceField(choices=Application.STATUS_TYPES)
    description = serializers.CharField(max_length=5000)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'image']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question', 'image']


class GroupsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    user = StudentUserSerializer()

    class Meta:
        model = Student
        fields = '__all__'
