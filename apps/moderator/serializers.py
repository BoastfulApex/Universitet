from rest_framework import serializers
from university.serializers import *
from users.serializers import *
from student.serializers import *
from university.models import Group
from .models import *


class StudentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone']


class ModeratorUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['phone', 'password', 'full_name', 'super_admin', 'create_subject', 'create_group_faculty_type',
                  'working_with_applicant', 'working_with_student', 'send_message', 'edit_group', 'finance']


class ModeratorSerializer(serializers.ModelSerializer):
    user = ModeratorUserSerializer()

    class Meta:
        model = Moderator
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        phone = user_data.pop('phone')
        name = user_data.pop('full_name')
        # Create the User instance
        user = User.objects.create_superuser(phone=phone, password=password)
        user.full_name = name
        user.edit_group = user_data.pop('edit_group')
        user.working_with_student = user_data.pop('working_with_student')
        user.working_with_applicant = user_data.pop('working_with_applicant')
        user.create_subject = user_data.pop('create_subject')
        user.super_admin = user_data.pop('super_admin')
        user.create_group_faculty_type = user_data.pop('create_group_faculty_type')
        user.send_message = user_data.pop('send_message')
        user.finance = user_data.pop('finance')
        user.analytica = user_data.pop('analytica')
        user.save()

        # Create the Moderator instance
        moderator = Moderator.objects.create(user=user, **validated_data)

        return moderator

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            instance.user = user

        return super().update(instance, validated_data)


class ApplicationSerializer(serializers.ModelSerializer):
    user = StudentUserSerializer()

    class Meta:
        model = Application
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        instance = self.Meta.model(**validated_data)

        if user_data:
            user_serializer = self.fields['user']
            user = user_serializer.create(user_data)
            instance.user = user

        instance.save()
        return instance

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = self.fields['user']
            user = instance.user
            user = user_serializer.update(user, user_data)
            instance.user = user

        return super().update(instance, validated_data)


class ApplicationDetailSerializer(serializers.ModelSerializer):

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
        fields = ['id', 'answer', 'image', 'is_correct']


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


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    student_id = serializers.CharField(max_length=200, required=False)
    groups = serializers.ListField(child=serializers.IntegerField())


class FinanceFileSerializer(serializers.Serializer):
    file = serializers.FileField()


class ApplicationListUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Application.STATUS_TYPES)
    objects = serializers.ListField(child=serializers.IntegerField())
    description = serializers.CharField(max_length=5000)

