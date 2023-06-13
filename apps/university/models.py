from django.db import models


class StudyType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class Faculty(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class FacultyType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)


