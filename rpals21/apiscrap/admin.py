from django.contrib import admin

# Register your models here.
from .models import RobotMonitor, TasksRobot


@admin.register(TasksRobot)
class TasksRobotAdminModel(admin.ModelAdmin):
    list_display = ('id', 'task_celey_id', 'task_label', 'robot_monitor', 'status',)
    list_filter = ('robot_monitor', 'status',)


@admin.register(RobotMonitor)
class RobotMonitorAdminModel(admin.ModelAdmin):
    list_display = ('id', 'search_key', 'started', 'finished', 'status', 'owner',)
    list_filter = ('owner', 'status',)
