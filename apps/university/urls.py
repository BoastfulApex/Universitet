from django.urls import path
from .views import *
from users.views import UserDataPostView

urlpatterns = [
    path('study_types/', StudyTypeListView.as_view(), name='study-types'),
    path('faculty/', FacultyListView.as_view(), name='faculty'),
    path('faculty_type/', FacultyTypeListView.as_view(), name='faculty-type'),
    path('user_data_post/', UserDataPostView.as_view(), name='user_data_post'),

]
