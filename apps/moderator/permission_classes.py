from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class CreateGroupFacultyType(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.create_group_faculty_type or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class CreateSubjectTest(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.create_subject  or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class WorkingStudent(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.working_with_student or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class WorkingApplicant(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif request.user.working_with_applicant or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class SendMessage(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.send_message or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class EditGroup(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.edit_group or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class Finance(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.finance or not request.user.super_admin:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True
