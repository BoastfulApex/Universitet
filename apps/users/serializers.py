from rest_framework import serializers
from .models import User

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class PhoneAuthTokenSerializer(serializers.Serializer):
    phone = serializers.CharField(
        label=_("Phone"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(request=self.context.get('request'),
                                phone=phone, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    full_name = serializers.CharField()

    # def validate(self, attrs):
    #     phone = attrs['phone']
    #     data = User.objects.filter(phone=phone).first()
    #     if not data:
    #         raise serializers.ValidationError({"Error": "Mijozlar bazasida bu telefon raqamga mos ma'lumotlar "
    #                                                     "topilmadi!"})
    #     return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone', 'otp')
