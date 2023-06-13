from django.contrib.auth.signals import user_logged_in
from knox.models import AuthToken

from django.contrib.auth import login

from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView

from rest_framework.response import Response
from rest_framework import generics

from .serializers import PhoneVerifySerializer, PhoneAuthTokenSerializer, UserSerializer
from .models import User


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

    def post(self, request, format=None):
        serializer = PhoneAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)

        return Response(
            {"status": True,
             "code": 200,
             "data": data,
             "message": []}
        )


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
