from django.contrib import admin
# Register your models here.
from .models import (
    Faculty, 
    FacultyType, 
    StudyType, 
    Subject,
    Question,
    Group
)



admin.site.register(Faculty)
admin.site.register(FacultyType)
admin.site.register(StudyType)
admin.site.register(Subject)
admin.site.register(Question)
admin.site.register(Group)