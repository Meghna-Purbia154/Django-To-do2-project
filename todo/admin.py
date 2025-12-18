from django.contrib import admin
from .models import Profile, Category, Task, SubTask, Notification

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Notification)
