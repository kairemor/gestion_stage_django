from django.contrib import admin
from .models import Student, Framer, Teacher, Task, ConventionMessage, Notification

# Register your models here.
admin.site.register(Student)
admin.site.register(Framer)
admin.site.register(Teacher)
admin.site.register(Task)
admin.site.register(ConventionMessage)
admin.site.register(Notification)
