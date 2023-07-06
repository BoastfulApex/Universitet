from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


class CreateGroupFacultyType(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.create_group_faculty_type or request.user.super_admin:
                return True
            else:
                return False
        return False


class CreateSubjectTest(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.create_subject or request.user.super_admin:
                return True
            else:
                return False
        return False


class WorkingStudent(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.working_with_student or request.user.super_admin:
                return True
            else:
                return False
        return False


class WorkingApplicant(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.working_with_applicant or request.user.super_admin:
                return True
            else:
                return False
        return False


class SendMessage(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.send_message or request.user.super_admin:
                return True
            else:
                return False
        return False


class EditGroup(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.edit_group or request.user.super_admin:
                return True
            else:
                return False
        return False


class Finance(BasePermission):

    def has_permission(self, request, view):
        if request.user.finance:
            if request.user.working_with_applicant or request.user.super_admin:
                return True
            else:
                return False
        return False
