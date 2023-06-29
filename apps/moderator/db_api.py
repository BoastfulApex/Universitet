from university.models import *
from student.models import *
from moderator.models import *


def get_valid_group_name(faculty_type):
    i = 1
    while True:
        group = Group.objects.filter(name=f"{faculty_type.group_name}-{i}")
        if not group:
            return f"{faculty_type.group_name}-{i}"
            break
        i += 1


def get_group_students_value(group):
    students = Student.objects.filter(group=group).all()
    return len(students)


def get_valid_group(faculty_type):
    group = Group.objects.filter(faculty_type=faculty_type).last()
    if group.students <= get_group_students_value(group):
        group = Group.objects.create(
            faculty_type = faculty_type,
            faculty=faculty_type.faculty,
            name=get_valid_group_name(faculty_type),
            students=faculty_type
        )
        group.save()

    return group
