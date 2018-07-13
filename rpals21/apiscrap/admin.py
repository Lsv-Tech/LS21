from django.contrib import admin

# Register your models here.
from .models import RobotMonitor, TasksRobot

admin.site.register(RobotMonitor)
admin.site.register(TasksRobot)
