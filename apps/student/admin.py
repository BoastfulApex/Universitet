from django.contrib import admin
from .models import (
    Test, 
    TestQuestion, 
    TestSubject, 
    Student, 
    Application
)

# Register your models here.
admin.site.register(Test)
admin.site.register(TestQuestion)
admin.site.register(TestSubject)
admin.site.register(Student)
admin.site.register(Application)