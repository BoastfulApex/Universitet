from django.urls import path
from .views import *
from users.views import *
#
# urlpatterns = [
#     path('study_types/', StudyTypeListView.as_view(), name='study-types'),
#     path('faculty/', FacultyListView.as_view(), name='faculty'),
#     path('faculty_type/', FacultyTypeListView.as_view(), name='faculty-type'),
#     path('user_registration/', UserRegistrationPostView.as_view(), name='user-registration'),
#     path('user_transfer/', UserTransferPostView.as_view(), name='user-transfer'),
#     path('application/', ApplicationView.as_view(), name='application-view'),
#     path('application_update/', ApplicationUpdateView.as_view(), name='application-update'),
#
# ]
