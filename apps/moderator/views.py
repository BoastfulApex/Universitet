from .serializers import *
from .paginators import ApplicationPagination
from rest_framework import generics, permissions
from rest_framework.response import Response
import requests
from student .models import Test, TestSubject, Student


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
    requests.post(url=url, headers={}, auth=(username, password), json=sms_data)


class ApplicationView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    # permission_classes = [permissions.IsAdminUser]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        queryset = Application.objects.all()
        application_type_mapping = {key: value for key, value in [
            ('register', 'Ro\'yxatdan o\'tish'),
            ('transfer', 'O\'qishni ko\'chirish'),
            ('consultation', 'Konsultatsiya'),
        ]}

        application_type = self.request.GET.get('type', None)
        test_type = self.request.GET.get('test', None)

        if application_type:
            queryset = queryset.filter(application_type__icontains=application_type_mapping.get(application_type))

        if test_type == 'passed':
            queryset = queryset.filter(test_passed=True)

        return queryset

        #     test = Test.objects.filter(application=application).first()
                #     subjects = TestSubject.objects.filter(test=test).all()
                #     for subject in subjects:
                #         all_ball += subject.ball
                #         sub = {
                #             'id': subject.id,
                #             'name': subject.subject.site_name,
                #             'ball': subject.ball,
                #             'correct_answers': subject.correct_answers,
                #             'wrong_answers': subject.wrong_answers,
                #         }
                #         subjects_d.append(sub)
                #     test_data = {
                #         'id': test.id,
                #         'guid': test.guid,
                #         'start_date': test.start_date,
                #         'end_date': test.finish_date,
                #         'ball': all_ball,
                #         'subjects': subjects_d
                #     }
                #     app_data = {
                #         'id': application.id,
                #         'user': application.user.id,
                #         'phone': application.user.phone,
                #         'second_phone': application.second_phone,
                #         'full_name': application.full_name,
                #         'study_type': application.study_type.id,
                #         'faculty': application.faculty.id,
                #         'type': application.type.id,
                #         'passport_seria': application.passport_seria if application.passport_seria else None,
                #         'date_if_birth': application.date_if_birth if application.date_if_birth else None,
                #         'diploma_seria': application.diploma_seria if application.diploma_seria else None,
                #         'diploma_picture': application.diploma_picture.url if application.diploma_picture else None,
                #         'acceptance_order': application.acceptance_order.url if application.acceptance_order else None,
                #         'ielts_picture': application.ielts_picture.url if application.ielts_picture else None,
                #         'course_order': application.course_order.url if application.course_order else None,
                #         'removal_order': application.removal_order.url if application.removal_order else None,
                #         'academic_certificate': application.academic_certificate.url if application.academic_certificate else None,
                #         'university_license': application.university_license.url if application.university_license else None,
                #         'university_accreditation': application.university_accreditation.url if application.university_accreditation else None,
                #         'application_type': application.application_type,
                #         'status': application.status,
                #         'description': application.description if application.description else None,
                #         'test_data': test_data,
                #     }
                #     data.append(app_data)
                # return Response(data)


class ApplicationObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    # permission_classes = [permissions.IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        application = Application.objects.filter(id=kwargs['pk']).first()
        subjects = TestSubject.objects.filter(test=test).all()
        all_ball = 0
        data = []
        subjects_d = []
        test = Test.objects.filter(application=application).first()
        if test:
            for subject in subjects:
                all_ball += subject.ball
                sub = {
                    'id': subject.id,
                    'name': subject.subject.site_name,
                    'ball': subject.ball,
                    'correct_answers': subject.correct_answers,
                    'wrong_answers': subject.wrong_answers,
                }
                subjects_d.append(sub)
            test_data = {
                'id': test.id,
                'guid': test.guid,
                'start_date': test.start_date,
                'end_date': test.finish_date,
                'ball': all_ball,
                'subjects': subjects_d
            }
        app_data = {
            'id': application.id,
            'user': application.user.id,
            'phone': application.user.phone,
            'second_phone': application.second_phone,
            'full_name': application.full_name,
            'study_type': application.study_type.id,
            'faculty': application.faculty.id,
            'type': application.type.id,
            'passport_seria': application.passport_seria if application.passport_seria else None,
            'date_if_birth': application.date_if_birth if application.date_if_birth else None,
            'diploma_seria': application.diploma_seria if application.diploma_seria else None,
            'diploma_picture': application.diploma_picture.url if application.diploma_picture else None,
            'acceptance_order': application.acceptance_order.url if application.acceptance_order else None,
            'ielts_picture': application.ielts_picture.url if application.ielts_picture else None,
            'course_order': application.course_order.url if application.course_order else None,
            'removal_order': application.removal_order.url if application.removal_order else None,
            'academic_certificate': application.academic_certificate.url if application.academic_certificate else None,
            'university_license': application.university_license.url if application.university_license else None,
            'university_accreditation': application.university_accreditation.url if application.university_accreditation else None,
            'application_type': application.application_type,
            'status': application.status,
            'description': application.description if application.description else None,
            'test_data': test_data,
        }
        return Response(app_data)


class ApplicationUpdateView(generics.CreateAPIView):
    serializer_class = ApplicationUpdateSerializer
    # permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        application = Application.objects.get(id=request.data['id'])
        application.status = request.data['status']
        text = f"Assalomu alaykum {application.full_name}. Sizning {application.application_type} uchun qoldirgan arizangiz"
        f" {application.status}!"
        if request.data['description']:
            text += f"Sabab: {request.data['description']}"
            application.description = request.data['description']
        application.save()
        if application.status == "Tasdiqlandi":
            student = Student.objects.create(user=application.user)
            student.study_type = application.study_type
            student.passport_seria = application.passport_seria
            student.faculty = application.faculty
            student.type = application.type
            student.diploma_picture = application.diploma_picture
            student.ielts_picture = application.ielts_picture
            student.acceptance_order = application.acceptance_order
            student.course_order = application.course_order
            student.removal_order = application.removal_order
            student.academic_certificate = application.academic_certificate
            student.university_license = application.university_license
            student.university_accreditation = application.university_accreditation
            student.save()
        text += "Toshkent iqtisodiyot va pedagogika instituti."
        send_sms(phone=application.user.phone, text=text)
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

