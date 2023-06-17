from rest_framework import serializers
from .models import *


class StudyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyType
        fields = '__all__'


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class FacultyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultyType
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
