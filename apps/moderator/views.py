from django.shortcuts import render
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
import requests


def send_sms(phone, status, application_type, name):
    username = 'onlineqabul'
    password = 'p7LnIrh+-Vw'
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003",
                      "sms": {
                          "originator": "3700",
                          "content": {
                              "text": f"Assalomu alaykum {name}. Sizning {application_type} uchun qoldirgan arizangiz"
                                      f" {status}! Toshkent iqtisodiyot va pedagogika instituti."}
                      }
                      }]
    }
    url = "http://91.204.239.44/broker-api/send"
    requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


class ApplicationView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Application.objects.all()
        application_type = self.request.GET.get('type')
        if application_type == 'register':
            return queryset.filter(application_type='Ro\'yxatdan o\'tish')
        elif application_type == 'transfer':
            return queryset.filter(application_type='O\'qishni ko\'chirish')
        elif application_type == 'consultation':
            return queryset.filter(application_type='Konsultatsiya')
        else:
            return queryset


class ApplicationObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    # permission_classes = [permissions.IsAdminUser]


class ApplicationUpdateView(generics.CreateAPIView):
    serializer_class = ApplicationUpdateSerializer
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        application = Application.objects.get(id=request.data['id'])
        application.status = request.data['status']
        application.save()
        send_sms(phone=application.user.phone, application_type=application.application_type, status=application.status,
                 name=application.user.full_name)
        return Response({'status': 'edited'})


class StudyTypeView(generics.ListCreateAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    # permission_classes = [permissions.IsAdminUser]


class StudyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    # permission_classes = [permissions.IsAdminUser]


class FacultyView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    # permission_classes = [permissions.IsAdminUser]


class FacultyObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    # permission_classes = [permissions.IsAdminUser]


class FacultyTypeView(generics.ListCreateAPIView):
    serializer_class = FacultyTypeSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = FacultyType.objects.all()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset


class FacultyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacultyType.objects.all()
    serializer_class = FacultyTypeSerializer
    # permission_classes = [permissions.IsAdminUser]


class SubjectView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    # permission_classes = [permissions.IsAdminUser]


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ListQuestionAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        try:
            subject_id = self.kwargs['subject_id']
            return Question.objects.filter(subject_id=subject_id).all()
        except:
            return []

    def list(self, request, *args, **kwargs):
        questions = self.get_queryset()
        data = []
        for question in questions:
            answers = Answer.objects.filter(question_id=question.id).all()
            ans = []
            for answer in answers:
                d = {
                    'id': answer.id,
                    'answer': answer.answer,
                }
                ans.append(d)
            d_q = {
                'id': question.id,
                'question': question.question,
                'answers': ans
            }
            data.append(d_q)

        return Response(data)

