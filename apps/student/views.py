from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import *


class UserRegistrationPostView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserTransferPostView(generics.CreateAPIView):
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudyTypeListView(generics.ListAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer


class FacultyListView(generics.ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyTypeListView(generics.ListAPIView):
    serializer_class = FacultyTypeSerializer

    def get_queryset(self):
        queryset = FacultyType.objects.all()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset
