from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import *
from rest_framework.response import Response
from university.models import Answer


class UserRegistrationPostView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserTransferPostView(generics.CreateAPIView):
    serializer_class = TransferSerializer
    # permission_classes = [permissions.IsAuthenticated]


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


class TestGenerate(generics.CreateAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subjects = []
        instance = serializer.save()

        # if instance.application.type.subject1 is not None:
        #     test_subject = TestSubject.objects.create(
        #         test=instance,
        #         subject=instance.application.type.subject1
        #
        #     )
        #     test_subject.save()
        #     subjects.append(test_subject)
        # if instance.application.type.subject2 is not None:
        #     test_subject = TestSubject.objects.create(
        #         test=instance,
        #         subject=instance.application.type.subject2
        #
        #     )
        #     test_subject.save()
        #     subjects.append(test_subject)
        # if instance.application.type.subject3 is not None:
        #     test_subject = TestSubject.objects.create(
        #         test=instance,
        #         subject=instance.application.type.subject3
        #
        #     )
        #     test_subject.save()
        #     subjects.append(test_subject)
        # if instance.application.type.subject4 is not None:
        #     test_subject = TestSubject.objects.create(
        #         test=instance,
        #         subject=instance.application.type.subject4
        #
        #     )
        #     test_subject.save()
        #     subjects.append(test_subject)
        # if instance.application.type.subject5 is not None:
        #     test_subject = TestSubject.objects.create(
        #         test=instance,
        #         subject=instance.application.type.subject5
        #     )
        #     test_subject.save()
        #     subjects.append(test_subject)

        for i in range(1, 6):
            subject = getattr(instance.application.type, f"subject{i}")
            if subject is not None:
                test_subject = TestSubject.objects.create(
                    test=instance,
                    subject=subject
                )
                test_subject.save()
                subjects.append(test_subject)
        # TestSubject.objects.bulk_create(subjects)
        data = []
        for subject in subjects:
            questions_data = []
            test_questions = TestQuestion.objects.filter(subject=subject).all()
            for test_question in test_questions:
                answers_data = []
                answers = Answer.objects.filter(question=test_question.question).order_by('?').all()
                for answer in answers:
                    answer_d = {
                        'id': answer.id,
                        'answer': answer.answer
                    }
                    answers_data.append(answer_d)
                question = {
                    'id': test_question.id,
                    'question': test_question.question.question,
                    'student_answer': test_question.studen_tanswer.id if test_question.student_answer else None,
                    'answers': answers_data
                }
                questions_data.append(question)
            subjects_data = {
                'id': subject.id,
                'name': subject.subject.site_name,
                'questions': questions_data
            }
            data.append(subjects_data)

        return Response(data, status=status.HTTP_201_CREATED)

