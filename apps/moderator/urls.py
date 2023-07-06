from django.urls import path
from .views import *
from users.views import *

urlpatterns = [
    path('study_types/', StudyTypeView.as_view(), name='study-types'),
    path('study_types/<int:pk>', StudyTypeObjectView.as_view(), name='study-types-object'),
    path('faculty/', FacultyView.as_view(), name='faculty'),
    path('faculty/<int:pk>', FacultyObjectView.as_view(), name='faculty-object'),
    path('faculty_type/', FacultyTypeView.as_view(), name='faculty-type'),
    path('faculty_type/<int:pk>', FacultyTypeObjectView.as_view(), name='faculty-type-object'),
    path('application/', ApplicationView.as_view(), name='application-view'),
    path('application/<int:pk>', ApplicationObjectView.as_view(), name='application-object'),
    path('application_update/', ApplicationUpdateView.as_view(), name='application-update'),
    path('subject/', SubjectView.as_view(), name='subject-view'),
    path('subject/<int:pk>', SubjectDetail.as_view(), name='subject-detail-view'),
    path('subject/<int:subject_id>/questions/', ListQuestionAPIView.as_view(), name='subject-questions'),
    path('answers/', AnswerView.as_view(), name='answers'),
    path('group/', GroupView.as_view(), name='group-view'),
    path('students/', StudentView.as_view(), name='students-view'),
    path('students/<int:pk>', StudentDetail.as_view(), name='students-detail'),
    path('group/<int:pk>', GroupDetail.as_view(), name='group-detail'),
    path('students_docs/', StudentsDoc.as_view(), name='students-docs'),

    path('create_moderator/', ModeratorView.as_view(), name='create_moderator'),
    path('send_message/', SendMessageView.as_view(), name='send_message_groups'),

    path('finance_file/', FinanceFileView.as_view(), name='finance_file'),

]

