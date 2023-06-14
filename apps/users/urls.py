from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path(r'phone_verify/', PhoneVerify.as_view(), name='phone_verify'),

]
