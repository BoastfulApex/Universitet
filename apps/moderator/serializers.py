from rest_framework import serializers
from university.serializers import *
from users.serializers import *
from student.serializers import *
from university.models import Group


class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone', 'full_name']


class ApplicationSerializer(serializers.ModelSerializer):
    # user = StudentUserSerializer()

    class Meta:
        model = Application
        fields = '__all__'

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user', None)
    #     if user_data:
    #         user_serializer = self.fields['user']
    #         user = instance.user
    #         user = user_serializer.update(user, user_data)
    #         instance.user = user

        return super().update(instance, validated_data)


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

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            instance.user = user

        return super().update(instance, validated_data)

