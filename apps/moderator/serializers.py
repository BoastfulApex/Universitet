from rest_framework import serializers
from university.serializers import *
from users.serializers import *
from student.serializers import Application


class ApplicationSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    def get_phone(self, obj):
        return obj.user.phone if obj.user else None

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
        fields = ('id', 'answer', 'image')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'question', 'image')
