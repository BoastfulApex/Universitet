from django.urls import path
from .views import *
from users.views import *

urlpatterns = [
    path('study_types/', StudyTypeView.as_view(), name='study-types'),
    path('faculty/', FacultyView.as_view(), name='faculty'),
    path('faculty_type/', FacultyTypeView.as_view(), name='faculty-type'),
    path('application/', ApplicationView.as_view(), name='application-view'),
    path('application_update/', ApplicationUpdateView.as_view(), name='application-update'),

]
