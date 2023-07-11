from django.urls import path
from .views import *
from users.views import *

urlpatterns = [
    path('study_types/', StudyTypeListView.as_view(), name='study-types'),
    path('faculty/', FacultyListView.as_view(), name='faculty'),
    path('faculty_type/', FacultyTypeListView.as_view(), name='faculty-type'),
    path('user_registration/', UserRegistrationPostView.as_view(), name='user-registration'),
    path('user_transfer/', UserTransferPostView.as_view(), name='user-transfer'),
    path('test/generate/', TestGenerate.as_view(), name='user-test-generate'),
    path('test/finish/', TestEnd.as_view(), name='user-finish'),
    path('test/answer/<int:pk>', StudentTestAnswer.as_view(), name='user-test-answer'),

    path('shartnoma/', StudentShartnomaView.as_view(), name='user-shartnoma'),
    path('malumotnoma/', StudentMalumotnomaView.as_view(), name='user-malumotnoma'),

]
