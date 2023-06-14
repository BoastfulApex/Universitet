from django.contrib.auth.signals import user_logged_in
from knox.models import AuthToken

from django.contrib.auth import login

from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView

from rest_framework.response import Response
from rest_framework import generics, status

from .serializers import *
from .models import User
from university.models import *

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.generate_otp()
        _, token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    serializers_class = PhoneAuthTokenSerializer


    def post(self, request, format=None):
        serializer = PhoneAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = {
            'token': token,
            'user': {
                'id': user.id,
                'phone': user.phone,
                'full_name': user.full_name,
            }
        }

        return Response(data)


class PhoneVerify(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = PhoneVerifySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(phone=request.data["phone"])
            user.generate_otp()
            return Response(
                {"status": True,
                 "code": 200,
                 "data": user.otp,
                 "message": []}
            )


class UserDataPostView(generics.CreateAPIView):
    serializer_class = UserDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            user.passport_seria = data['passport_seria']
            user.full_name = data['full_name']
            user.date_if_birth = data['date_if_birth']
            user.diploma_picture = data['diploma_picture']
            user.ielts_picture = data['ielts_picture']
            user.save()
            return Response({'status': 'created'})
        except Exception as exx:
            return Response({"error": str(exx)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)