from .serializers import *
from .paginators import ApplicationPagination
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
import requests
from student.models import Test, TestSubject, Student, StudentFinance
from .db_api import *
import pandas as pd
from .permission_classes import *


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


class ApplicationView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [WorkingApplicant]
    pagination_class = ApplicationPagination

    def get_queryset(self):
        application_type_mapping = {key: value for key, value in [
            ('register', 'Ro\'yxatdan o\'tish'),
            ('transfer', 'O\'qishni ko\'chirish'),
            ('consultation', 'Konsultatsiya'),
        ]}
        queryset = Application.objects.all()
        application_type = self.request.GET.get('type', None)
        test_type = self.request.GET.get('test', None)

        if application_type:
            queryset = queryset.filter(application_type__icontains=application_type_mapping.get(application_type))

        if test_type == 'passed':
            queryset = queryset.filter(test_passed=True)

        return queryset


class ApplicationObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    permission_classes = [WorkingApplicant]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        all_ball = 0
        subjects_d = []
        test_data = []
        test = Test.objects.filter(application=instance).first()
        if test:
            subjects = TestSubject.objects.filter(test=test).all()
            for subject in subjects:
                all_ball += subject.ball
                sub = {
                    'id': subject.id,
                    'name': subject.subject.site_name,
                    'ball': subject.ball,
                    'correct_answers': subject.correct_answers,
                    'wrong_answers': subject.wrong_answers,
                    'all_questions': subject.correct_answers + subject.wrong_answers
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
        data = serializer.data
        data['test'] = test_data
        return Response(data)


class ApplicationUpdateView(generics.CreateAPIView):
    serializer_class = ApplicationUpdateSerializer

    permission_classes = [WorkingApplicant]

    def post(self, request, *args, **kwargs):
        application = Application.objects.get(id=request.data['id'])
        application.status = request.data['status']
        text = f"Assalomu alaykum {application.user.full_name}." \
               f" Sizning {application.application_type} uchun qoldirgan arizangiz {application.status}!"
        if request.data['description']:
            text += f"Sabab: {request.data['description']}"
            application.description = request.data['description']
        application.save()
        if application.application_type != "Konsultatsiya" and application.status == "Tasdiqlandi":
            student, created = Student.objects.get_or_create(user=application.user)
            student.study_type = application.study_type
            student.passport_seria = application.passport_seria
            student.faculty = application.faculty
            student.full_name = application.full_name
            student.type = application.type
            student.diploma_picture = application.diploma_picture
            student.diploma_seria = application.diploma_seria
            student.ielts_picture = application.ielts_picture
            student.acceptance_order = application.acceptance_order
            student.course_order = application.course_order
            student.removal_order = application.removal_order
            student.academic_certificate = application.academic_certificate
            student.university_license = application.university_license
            student.university_accreditation = application.university_accreditation
            student.group = get_valid_group(faculty_type=application.type, kurs=application.kurs_for)
            student.save()
        text += ""
        send_sms(phone=application.user.phone, text=text)
        return Response({'status': 'edited'})


class StudyTypeView(generics.ListCreateAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    permission_classes = [CreateGroupFacultyType]


class StudyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudyType.objects.all()
    serializer_class = StudyTypeSerializer
    permission_classes = [CreateGroupFacultyType]


class FacultyView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [CreateGroupFacultyType]


class FacultyObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [CreateGroupFacultyType]


class FacultyTypeView(generics.ListCreateAPIView):
    serializer_class = FacultyTypeSerializer

    permission_classes = [CreateGroupFacultyType]

    def get_queryset(self):
        queryset = FacultyType.objects.all()
        faculty_id = self.request.GET.get('faculty_id')
        if faculty_id:
            queryset = queryset.filter(faculty_id=faculty_id)

        return queryset


class FacultyTypeObjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FacultyType.objects.all()
    serializer_class = FacultyTypeSerializer
    permission_classes = [CreateGroupFacultyType]


class SubjectView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [CreateSubjectTest]


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [CreateSubjectTest]


class ListQuestionAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [CreateSubjectTest]

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


class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer

    permission_classes = [CreateGroupFacultyType]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save()
        headers = self.get_success_headers(serializer.data)
        group.faculty_type.group_name = group.name
        group.faculty_type.group_students = group.students
        group.faculty_type.save()
        group.name = get_valid_group_name(group.faculty_type)
        group.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [CreateGroupFacultyType, EditGroup]


class StudentView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer
    pagination_class = ApplicationPagination
    filter_backends = [SearchFilter]
    search_fields = ['user__full_name', 'user__phone', 'passport_seria']

    # permission_classes = [WorkingStudent]

    def get_queryset(self):
        queryset = Student.objects.all()
        group_id = self.request.GET.get('group_id')
        pay_type = self.request.GET.get('pay_type') if 'pay_type' in self.request.GET else None
        response_students = []
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if pay_type == "payed":
            for student in queryset:
                student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
                if sum(student_pays) >= (student.type.contract_amount1 + student.type.contract_amount2):
                    response_students.append(student)
            queryset = response_students
        if pay_type == "not_payed":
            for student in queryset:
                student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
                if sum(student_pays) < (student.type.contract_amount1 + student.type.contract_amount2):
                    response_students.append(student)
            queryset = response_students
        if pay_type == "pay_date":
            for student in queryset:
                from datetime import date
                today = date.today()
                difference = student.type.first_quarter - today
                if difference.days < 10:
                    response_students.append(student)
            queryset = response_students
        return queryset


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = [WorkingStudent]


class StudentsDoc(generics.ListAPIView):
    serializer_class = StudentsSerializer
    permission_classes = [WorkingStudent]

    def get_queryset(self):

        queryset = Student.objects.all()
        group_id = self.request.GET.get('group_id')
        pay_type = self.request.GET.get('pay_type') if 'pay_type' in self.request.GET else None
        response_students = []
        if group_id:
            queryset = queryset.filter(group_id=group_id)
        if pay_type == "payed":
            for student in queryset:
                student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
                if sum(student_pays) >= (student.type.contract_amount1 + student.type.contract_amount2):
                    response_students.append(student)
            queryset = response_students
        if pay_type == "not_payed":
            for student in queryset:
                student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
                if sum(student_pays) < (student.type.contract_amount1 + student.type.contract_amount2):
                    response_students.append(student)
            queryset = response_students
        if pay_type == "pay_date":
            for student in queryset:
                from datetime import date
                today = date.today()
                difference = student.type.first_quarter - today
                if difference.days < 10:
                    response_students.append(student)
            queryset = response_students
        return queryset

    def list(self, request, *args, **kwargs):
        students = self.get_queryset()
        names = []
        phones = []
        passport_series = []
        diploma_series = []
        faculties = []
        faculty_types = []
        study_types = []
        groups = []
        for student in students:
            names.append(student.user.full_name)
            phones.append(student.user.phone)
            passport_series.append(student.passport_seria)
            diploma_series.append(student.diploma_seria)
            faculties.append(student.faculty.admin_name if student.faculty else None)
            study_types.append(student.study_type.name if student.study_type else None)
            faculty_types.append(student.type.name if student.type else None)
            groups.append(student.group.name if student.group else None)

        df = pd.DataFrame({
            "Ismi": names,
            "Telefon raqami": phones,
            "Fakultet": faculties,
            "Yo'nalish": faculty_types,
            "O'qish turi": study_types,
            "Guruh": groups,
            "Passport seria": passport_series,
            "Diplom": diploma_series,
        })
        df.to_excel('./files/xisobot.xlsx')

        return Response({'status': 'ok', 'file': "http://185.65.202.40:1009/files/xisobot.xlsx"})


class AnswerView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [CreateGroupFacultyType]

    def get_queryset(self):
        return Answer.objects.all()


class ModeratorView(generics.ListCreateAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    # permission_classes = [SuperAdmin]


class ModeratorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Moderator.objects.all()
    serializer_class = ModeratorSerializer
    permission_classes = [SuperAdmin]


class SendMessageView(generics.CreateAPIView):
    serializer_class = SendMessageSerializer
    permission_classes = [SendMessage]

    def create(self, request, *args, **kwargs):
        my_list = request.data['groups']
        groups = Group.objects.filter(id__in=my_list).all()
        for group in groups:
            students = Student.objects.filter(group=group).all()
            for student in students:
                send_sms(phone=student.user.phone, text=request.data['message'])
        if request.data['student_id']:
            student = Student.objects.filter(id=request.data['student_id']).first()
            if student:
                send_sms(phone=student.user.phone, text=request.data['message'])
        return Response({"status": "Success"})


class FinanceFileView(generics.CreateAPIView):
    serializer_class = FinanceFileSerializer
    permission_classes = [Finance]

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        with open('./files/xisobot-finance.xlsx', 'wb') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)
        file_path = open('./files/xisobot-finance.xlsx', 'rb')
        df = pd.read_excel(file_path)

        for i in df.index:
            str_agreement = df['Назначение платежа'][i]
            try:
                agreement_id = str(str_agreement).split('№0/9 ')[1][:5]
                student = Student.objects.filter(user_finance_id=agreement_id).first()
                if student:
                    pay = StudentFinence.objects.create(
                        student=student,
                        summa=int(df['Оборот керидит'][i])
                    )
                    pay.save()
            except:
                pass
        return Response({'status': "finance file added"})


class DashboardView(generics.ListAPIView):
    permission_classes = [Analytica]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        register_application = Application.objects.all()
        groups = Group.objects.all()
        faculty = Faculty.objects.all()
        faculty_type = FacultyType.objects.all()
        all_need_summa = 0
        students = Student.objects.all()
        confirmed_applications = Application.objects.filter(status='Tasdiqlandi').all()
        canceled_applications = Application.objects.filter(status='Rad etildi').all()
        all_pays = StudentFinance.objects.all()
        pays = [pay['summa'] for pay in all_pays]
        payed_1 = 0
        not_pay1 = 0
        not_pay2 = 0
        pay1 = 0
        pay2 = 0
        payed_2 = 0
        not_payed_1 = 0
        not_payed_2 = 0
        for student in students:
            student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
            if sum(student_pays) < student.type.contract_amount1:
                not_pay1 += student.type.contract_amount1 - sum(student_pays)
                not_pay2 += student.type.contract_amount2
                not_payed_1 += 1
                not_payed_2 += 1
            else:
                payed_1 += 1
                pay1 += student.type.contract_amount1
                if sum(student_pays) >= student.type.contract_amount2 + student.type.contract_amount2:
                    payed_2 += 1
                    pay2 += student.type.contract_amount2
                else:
                    print(sum(student_pays))
                    p = sum(student_pays) - student.type.contract_amount2 - student.type.contract_amount2
                    not_pay2 += p
                    not_payed_2 += 1
        finances = StudentFinance.objects.all()
        all_summ_finance = [pay.summa for pay in StudentFinance.objects.filter().all()]
        for i in faculty_type:
            all_need_summa += i.contract_amount2 + i.contract_amount1
        return Response(
            {
                'applications': len(register_application),
                'confirmed_applications': len(confirmed_applications),
                'canceled_applications': len(canceled_applications),
                'pays': sum(pays),
                'students': len(students),
                'faculty_type': len(faculty_type),
                'groups': len(groups),
                'faculty': len(faculty),
                'payed_1': payed_1,
                'payed_2': payed_2,
                'not_payed_1': not_payed_1,
                'not_payed_2': not_payed_2,
                'pay1': pay1,
                'pay2': pay2,
                'not_pay1': not_pay1,
                'not_pay2': not_pay2,
                'all_summ_finance': sum(all_summ_finance),
                'all_need_summa': all_need_summa - sum(pays)
            }
        )


class NotPayedStudent(generics.ListAPIView):
    permission_classes = [Analytica]

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        students = Student.objects.all()
        not_pay1 = []
        not_pay2 = []
        for student in students:
            student_pays = [pay.summa for pay in StudentFinance.objects.filter(student=student).all()]
            if sum(student_pays) < student.type.contract_amount1:
                not_pay1.append(student)
                not_pay2.append(student)
            elif sum(student_pays) >= student.type.contract_amount2 + student.type.contract_amount2:
                pass
            else:
                not_pay2.append(student)
        return Response(
            {
                "not_pay_2": not_pay2,
                "not_pay_1": not_pay1,
            }
        )


class FacultyTypeAddView(generics.CreateAPIView):
    serializer_class = FinanceFileSerializer

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        with open('./files/faculty_type-file.xlsx', 'wb') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)
        file_path = open('./files/faculty_type-file.xlsx', 'rb')
        df = pd.read_excel(file_path)
        response_data = []
        for i in df.index:
            faculty_name = df['Fakultet'][i]
            faculty, created = Faculty.objects.get(
                admin_name=faculty_name
            )
            faculty.site_name = faculty_name
            faculty.save()
            type_name = df["Yo'nalish"][i]
            type, create = FacultyType.objects.get_or_create(
                faculty=faculty,
                name=name
            )
            faculty_data = {
                'id': faculty.id,
                'admin_name': faculty.admin_name,
                'site_name': faculty.site_name
            }
            response_data.append(faculty_data)
        return Response(response_data)


class StudentFileAddView(generics.CreateAPIView):
    serializer_class = FinanceFileSerializer
    permission_classes = [WorkingApplicant]

    def get_queryset(self):
        return []

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        with open('./files/faculty_type-file.xlsx', 'wb') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)
        file_path = open('./files/faculty_type-file.xlsx', 'rb')
        df = pd.read_excel(file_path)
        response_data = []
        for i in df.index:
            check = False
            phone = df['Telefon Raqam'][i]
            user, created = User.objects.get_or_create(
                phone=phone
            )
            user.save()
            faculty_name = df['Fakultet'][i]
            faculty = Faculty.objects.filter(admin_name=faculty_name).first()
            type_name = df["Yo'nalish"][i]
            faculty_type = FacultyType.objects.filter(name=type_name).first()
            if faculty_type != [] and faculty != []:
                study_type = StudyType.objects.filter(name=df["O'qish turi"][i]).first()
                applicant, created = Application.objects.get_or_create(
                    user=user,
                )
                applicant.phone = df['Telefon Raqam'][i]
                applicant.faculty = faculty
                applicant.type = faculty_type
                applicant.study_type = study_type
                applicant.passport_seria = df['Passport']
                applicant.full_name = df['Ism']
                applicant.save()
                applicant_data = {
                    'id': applicant.id,
                    'user': {
                        'phone': applicant.user.phone
                    },
                    'phone': applicant.phone,
                    'faculty': applicant.faculty.id,
                    'type': applicant.type.id,
                    'study_type': applicant.study_type.id,

                }
                response_data.append(applicant_data)
        return Response(response_data)


class ApplicationListUpdateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = ApplicationListUpdateSerializer
    permission_classes = [WorkingApplicant]

    def post(self, request, *args, **kwargs):
        for app_id in request.data['objects']:
            application = Application.objects.filter(id=app_id).first()
            if application:
                application.status = request.data['status']
                text = f"Assalomu alaykum {application.user.full_name}." \
                       f" Sizning {application.application_type} uchun qoldirgan arizangiz {application.status}!"
                if request.data['description']:
                    text += f"Sabab: {request.data['description']}"
                    application.description = request.data['description']
                application.save()
                if application.application_type != "Konsultatsiya" and application.status == "Tasdiqlandi":
                    student, created = Student.objects.get_or_create(user=application.user)
                    student.study_type = application.study_type
                    student.passport_seria = application.passport_seria
                    student.faculty = application.faculty
                    student.full_name = application.full_name
                    student.type = application.type
                    student.diploma_picture = application.diploma_picture
                    student.diploma_seria = application.diploma_seria
                    student.ielts_picture = application.ielts_picture
                    student.acceptance_order = application.acceptance_order
                    student.course_order = application.course_order
                    student.removal_order = application.removal_order
                    student.academic_certificate = application.academic_certificate
                    student.university_license = application.university_license
                    student.university_accreditation = application.university_accreditation
                    student.group = get_valid_group(application.type, kurs=application.kurs_for)
                    student.save()
                text += ""
                send_sms(phone=application.user.phone, text=text)
        return Response({'status': 'edited'})


class ModeratorPermissions(generics.ListAPIView):
    serializer_class = ModeratorSerializer
    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Moderator.objects.filter(user=self.request.user)
        return queryset


class ChangeYear(generics.ListAPIView):
    serializer_class = ApplicationListUpdateSerializer
    permission_classes = [SuperAdmin]
    
    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        for group in Group.objects.all():
            if group.course != '4-Kurs':
                kurs = int(group.course.split('-')[0])
                group.course = f"{kurs + 1}-Kurs"
            else:
                group.course = "Tugallagan"
            group.save()


class DeleteFor(generics.ListAPIView):
    serializer_class = StudentsSerializer

    def get_queryset(self):
        return []

    def list(self, request, *args, **kwargs):
        applications = Application.objects.all()
        for i in applications:
            if i.id != 32:
                i.delete()
