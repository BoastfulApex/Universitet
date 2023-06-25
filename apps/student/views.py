import datetime

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

    def list(self, request, *args, **kwargs):
        tests = Test.objects.all()
        for t in tests:
            t.delete()


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


class TestGenerate(generics.ListCreateAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        guid = self.request.GET.get('guid')
        data = []
        # try:
        test = Test.objects.get(guid=guid)
        test.start_date = datetime.datetime.now()
        test.save()

        subjects = TestSubject.objects.filter(test=test)
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
        # except:
        #     pass
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subjects = []
        instance = serializer.save()
        for i in range(1, 6):
            subject = getattr(instance.application.type, f"subject{i}")
            if subject is not None:
                test_subject = TestSubject.objects.create(
                    test=instance,
                    subject=subject
                )
                test_subject.save()
                subjects.append(test_subject)
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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentTestAnswer(generics.UpdateAPIView):
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        return []

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.student_answer and instance.student_answer.is_correct:
            if not instance.solved:
                instance.solved = True
                instance.subject.correct_answers += 1
                instance.subject.wrong_answers -= 1
                instance.subject.ball += self.subject.subject.one_question_ball
                instance.subject.save()
                instance.save()


class TestEnd(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        guid = self.request.GET.get('guid')
        data = []
        test = Test.objects.get(guid=guid)
        test.end_date = datetime.datetime.now()
        test.save()
        subjects = TestSubject.objects.filter(test=test)
        for subject in subjects:
            sub = {
                'id': subject.id,
                'name': subject.site_name,
                'ball': subject.ball,
                'correct_answers': subject.correct_answers,
                'wrong_answers': subject.wrong_answers,
            }
            data.append(sub)

        return Response(data)