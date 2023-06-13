from django.shortcuts import render
from rest_framework import generics
from .models import StudyType, Faculty, FacultyType
from .serializers import StudyTypeSerializer, FacultySerializer, FacultyTypeSerializer


class StudyTypeListView(generics.ListAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer


class FacultyListView(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyTypeListView(generics.ListAPIView):
    serializer_class = FacultyTypeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset
