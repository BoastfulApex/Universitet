import datetime
import pytz
from django.shortcuts import render
from rest_framework import generics, status, permissions
from .serializers import *
from rest_framework.response import Response
from university.models import Answer, get_random_choice
import random
import requests
from .shartnoma import create_shartnoma
from django.core.files import File


def send_sms(phone, text):
    username = 'onlineqabul'
    password = 'p7LnIrh+-Vw'
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003",
                      "sms": {
                          "originator": "3700",
                          "content": {
                              "text": text}
                      }
                      }]
    }
    url = "http://91.204.239.44/broker-api/send"
    res = requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


class UserRegistrationPostView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    # permission_classes = [permissions.IsAuthenticated]


class UserTransferPostView(generics.CreateAPIView):
    serializer_class = TransferSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # def perform_create(self, serializer):
    #     # Get the validated data from the serializer
    #     validated_data = serializer.validated_data
    #
    #     # Extract the unique identifier field from the validated data
    #     identifier = validated_data.get('user')
    #     # Perform the get_or_create operation
    #     instance, created = Application.objects.get_or_create(user=identifier, defaults=validated_data)
    #     instance.status = "Ko'rib chiqilmoqda"
    #     # Set the instance as the created obj ect and save it
    #     serializer.instance = instance
    #     serializer.save()


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


class TestGenerate(generics.ListCreateAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        guid = self.request.GET.get('guid')
        data = []
        test_d = []
        try:
            test = Test.objects.get(guid=guid)
            if not test.start_date:
                test.start_date = datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
                test.finish_date = test.start_date + datetime.timedelta(minutes=test.application.type.test_minute)
            test.save()
            remain_date = test.finish_date - datetime.datetime.now(pytz.timezone('Asia/Tashkent'))
            until = remain_date.total_seconds() // 60 + 1
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
                            'answer': answer.answer,
                            'answer_image': answer.image if answer.image else None
                        }
                        answers_data.append(answer_d)
                    question = {
                        'id': test_question.id,
                        'question': test_question.question.question,
                        'question_image': test_question.question.image if test_question.question.image else None,
                        'student_answer': test_question.studenT_answer.id if test_question.student_answer else None,
                        'answers': answers_data
                    }
                    questions_data.append(question)
                subjects_data = {
                    'id': subject.id,
                    'name': subject.subject.site_name,
                    'questions': questions_data
                }
                data.append(subjects_data)
            test_d = {
                'id': test.id,
                'guid': test.guid,
                'start_date': test.start_date,
                'finish_date': test.finish_date,
                'qolgan_vaqt': until,
                'ball': 0,
                'data': data
            }
        except:
            pass
        return Response(test_d)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        application = request.data['application']
        test = Test.objects.filter(application_id=application).first()
        if not test:
            subjects = []
            serializer.is_valid()
            instance = serializer.save()
            for i in range(1, 6):
                subject = getattr(instance.application.type, f"subject{i}")
                if subject is not None:
                    test_subject = TestSubject.objects.create(
                        test=instance,
                        subject=subject,
                        wrong_answers=subject.question_number
                    )
                    test_subject.save()
                    for j in range(0, subject.question_number):
                        questions = Question.objects.filter(subject=subject)
                        test_question = TestQuestion.objects.create(
                            subject=test_subject,
                            question=random.choice(questions)
                        )
                        test_question.save()
                    subjects.append(test_subject)
            data = []
            for subject_i in subjects:
                subjects_data = {
                    'id': subject_i.id,
                    'name': subject_i.subject.site_name,
                    'questions': subject_i.subject.question_number
                }
                data.append(subjects_data)
            response_data = serializer.data
            response_data['subjects'] = data
            response_data['interval'] = instance.application.type.test_minute
            text = f"Sizning test yechish manzilingiz: http://tivpi.uz/test/before/{instance.application.id}" \
                   f"?guid={instance.guid}. Toshkent iqtisodiyot va " \
                   "pedagogika instituti."
            send_sms(phone=instance.application.user.phone, text=text)

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            subjects = TestSubject.objects.filter(test=test)
            data = []
            for subject_i in subjects:
                subjects_data = {
                    'id': subject_i.id,
                    'name': subject_i.subject.site_name,
                    'questions': subject_i.subject.question_number
                }
                data.append(subjects_data)
            test_d = {
                'id': test.id,
                'guid': test.guid,
                'start_date': test.start_date,
                'finish_date': test.finish_date,
                'ball': 0,
                'subjects': data,
                'interval': test.application.type.test_minute
            }
            return Response(test_d)


class StudentTestAnswer(generics.UpdateAPIView):
    serializer_class = StudentAnswerSerializer

    def get_queryset(self):
        return []

    def update(self, request, *args, **kwargs):
        test_question = TestQuestion.objects.get(id=kwargs['pk'])
        answer = Answer.objects.get(id=request.data['student_answer'])
        test_question.student_answer = answer
        test_question.save()
        if test_question.student_answer and test_question.student_answer.is_correct:
            if not test_question.solved:
                test_question.solved = True
                test_question.subject.correct_answers += 1
                test_question.subject.wrong_answers -= 1
                test_question.subject.ball += test_question.subject.subject.one_question_ball
                test_question.subject.save()
                test_question.save()
        return Response([])


class TestEnd(generics.ListAPIView):
    serializer_class = TestSerializer

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        guid = request.GET.get('guid')
        data = []
        test = Test.objects.filter(guid=guid).first()
        if test:
            test.finish_date = datetime.datetime.now()
            test.save()
            all_ball = 0
            subjects_d = []
            subjects = TestSubject.objects.filter(test=test)
            for subject in subjects:
                sub = {
                    'id': subject.id,
                    'name': subject.subject.site_name,
                    'ball': subject.ball,
                    'correct_answers': subject.correct_answers,
                    'wrong_answers': subject.wrong_answers,
                    'all': subject.wrong_answers + subject.correct_answers,
                }
                subjects_d.append(sub)
                all_ball += subject.ball
            test.application.test_passed = True
            test.application.save()

            data = {
                'id': test.id,
                'guid': test.guid,
                'start_date': test.start_date,
                'end_date': test.finish_date,
                'ball': all_ball,
                'subjects': subjects_d
            }
            return Response(data)
        else:
            return Response([])


class StudentShartnomaView(generics.CreateAPIView):
    serializer_class = ShartnomaSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        try:

            student = Student.objects.filter(passport_seria=request.data['passport']).first()
            if student:
                agreement = Agreement.objects.filter(student=student).first()
                from datetime import date
                today = date.today()
                formatted_date = today.strftime('%d.%m.%Y')
                template = student.type.shartnoma_file.url
                create_shartnoma(id=student.user_finance_id, name=student.full_name, mode=student.study_type.name,
                                 passport=student.passport_seria, faculty=student.faculty.site_name, template=template,
                                 number=student.user.phone, price=student.type.contract_amount, date=formatted_date)
                agreement = Agreement.objects.create(
                    student=student
                )
                agreement.file_path = f'http://185.65.202.40:1009/files/agreements/{student.user_finance_id}.pdf'
                agreement.save()
                return Response({"shartnoma": agreement.file_path})
            else:
                return Response({})
        except Exception as exx:
            return Response([])


class StudentMalumotnomaView(generics.CreateAPIView):
    serializer_class = ShartnomaSerializer

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        student = Student.objects.filter(passport_seria=request.data['passport']).first()
        if student:
            from datetime import date
            today = date.today()
            formatted_date = today.strftime('%d.%m.%Y')
            template = student.type.shartnoma_file.url
            create_shartnoma(id=student.user.guid, name=student.full_name, mode=student.study_type.name,
                             passport=student.passport_seria, faculty=student.faculty.site_name, template=template,
                             number=student.user.phone, price=student.type.contract_amount, date=formatted_date)
            agreement = Agreement.objects.create(
                student=student,
            )
            agreement.file_path = f'http://185.65.202.40:1009/files/agreements/{student.user.guid}.pdf'
            agreement.save()
            return Response({"shartnoma": agreement.file_path})
        else:
            return Response({})
