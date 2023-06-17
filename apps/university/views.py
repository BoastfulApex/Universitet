from rest_framework import generics
from .models import StudyType, Faculty, FacultyType
from .serializers import StudyTypeSerializer, FacultySerializer, FacultyTypeSerializer
from users.permissions import IsSuperuserOrReadOnly
