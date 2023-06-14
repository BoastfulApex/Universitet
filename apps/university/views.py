from rest_framework import generics
from .models import StudyType, Faculty, FacultyType
from .serializers import StudyTypeSerializer, FacultySerializer, FacultyTypeSerializer
from users.permissions import IsSuperuserOrReadOnly


class StudyTypeListView(generics.ListCreateAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    permission_classes = [IsSuperuserOrReadOnly]


class FacultyListView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsSuperuserOrReadOnly]


class FacultyTypeListView(generics.ListCreateAPIView):
    serializer_class = FacultyTypeSerializer
    permission_classes = [IsSuperuserOrReadOnly]

    def get_queryset(self):
        queryset = FacultyType.objects.all()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset
