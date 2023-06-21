from django.db import models


class StudyType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class Faculty(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)


class FacultyType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    subject1 = models.ForeignKey('university.Subject', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='first_subject')
    subject2 = models.ForeignKey('university.Subject', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='second_subject')
    subject3 = models.ForeignKey('university.Subject', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='third_subject')
    subject4 = models.ForeignKey('university.Subject', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='fourth_subject')
    subject5 = models.ForeignKey('university.Subject', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='fifth_subject')
    passing_score = models.IntegerField(default=0)


class Subject(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    passing_score = models.IntegerField(null=True)
    test_file = models.FileField(null=True, blank=True)

    def __str__(self):
        try:
            return self.name
        except:
            return self.id


class Question(models.Model):
    question = models.CharField(max_length=5000, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=5000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)


