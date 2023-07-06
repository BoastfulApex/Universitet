from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class CreateGroupFacultyType(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.create_group_faculty_type:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class CreateSubjectTest(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.create_subject:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class WorkingStudent(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.working_with_student:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class WorkingApplicant(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif request.user.working_with_applicant:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class SendMessage(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.send_message:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class EditGroup(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.edit_group:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True


class Finance(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        elif not request.user.finance:
            raise AuthenticationFailed(detail='Foydalanuvchi uchun ruxsat mavjud emas!!!', code=401)
        return True
