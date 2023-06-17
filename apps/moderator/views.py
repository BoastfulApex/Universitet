from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions


class ApplicationView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Application.objects.all()
        application_type = self.request.GET.get('type')
        if application_type == 'register':
            return queryset.filter(application_type='Ro\'yxatdan o\'tish')
        elif application_type == 'transfer':
            return queryset.filter(application_type='O\'qishni ko\'chirish')
        else:
            return []


class ApplicationObjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAdminUser]


class ApplicationUpdateView(generics.CreateAPIView):
    serializer_class = ApplicationUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        application = Application.objects.get(id=request.data['id'])
        application.status = request.data['status']
        application.save()
        return Response({'status': 'edited'})


class StudyTypeView(generics.ListCreateAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class StudyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class FacultyView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAdminUser]


class FacultyObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAdminUser]


class FacultyTypeView(generics.ListCreateAPIView):
    serializer_class = FacultyTypeSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = FacultyType.objects.all()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset


class FacultyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacultyType.objects.all()
    serializer_class = FacultyTypeSerializer
    permission_classes = [permissions.IsAdminUser]

