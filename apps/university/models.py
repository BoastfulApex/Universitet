from django.db import models
import pandas as pd
from PIL import Image
from io import BytesIO


class StudyType(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)


class Faculty(models.Model):
    admin_name = models.CharField(max_length=500, null=True, blank=True)
    site_name = models.CharField(max_length=500, null=True, blank=True)
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

    def check_privilege(self):
        if self.subject1:
            return False
        if self.subject2:
            return False
        if self.subject3:
            return False
        if self.subject4:
            return False
        if self.subject5:
            return False
        return True


class Question(models.Model):
    question = models.CharField(max_length=5000, null=True, blank=True)
    subject = models.ForeignKey('university.Subject', on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.CharField(max_length=5000, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)


class Subject(models.Model):
    admin_name = models.CharField(max_length=500, null=True, blank=True)
    site_name = models.CharField(max_length=500, null=True, blank=True)
    one_question_ball = models.IntegerField(null=True)
    test_file = models.FileField(null=True, blank=True)
    question_number = models.IntegerField(null=True)

    def __str__(self):
        try:
            return self.name
        except:
            return self.id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.test_file:
            file_path = self.test_file.path
            df = pd.read_excel(file_path)

            for i in df.index:
                question_text = df['Savol'][i]
                question_image = df['Rasm'][i]

                question = Question.objects.create(subject=self)
                question.question = question_text
                if pd.notna(question_image):  # Check if the cell contains an image
                    image = Image.open(BytesIO(question_image))
                    image_path = f'./files/question_images/{self.id}_{question.id}.jpg'  # Adjust the path as desired
                    image.save(image_path)
                    question.question_image = image_path
                question.save()

                # Save answers
                for j in range(1, 5):
                    answer_text = df[f'{j}-Javob'][i]
                    answer_image = df[f'{j}-Rasm'][i]
                    answer = Answer.objects.create(question=question, answer=answer_text)

                    if pd.notna(answer_image):
                        image = Image.open(BytesIO(answer_image))
                        image_path = f'./files/answer_images/{self.id}_{question.id}_{j}.jpg'
                        image.save(image_path)
                        answer.answer_image = image_path

                    answer.save()
