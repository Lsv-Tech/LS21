from django.contrib.auth.models import User
from rest_framework import serializers

from .models import RobotMonitor, TasksRobot


class UserModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RobotModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner_obj = serializers.SerializerMethodField()

    class Meta:
        model = RobotMonitor
        fields = ('id', 'started', 'search_key', 'finished', 'owner', 'owner_obj')

    def get_owner_obj(self, obj):
        return UserModelSerializer(obj.owner).data


class TaskRobotModelSerializer(serializers.ModelSerializer):
    robot_monitor_obj = serializers.SerializerMethodField()

    class Meta:
        model = TasksRobot
        fields = ('task_celey_id', 'task_label', 'status', 'result', 'robot_monitor', 'robot_monitor_obj',)

    def get_robot_monitor_obj(self, obj):
        return RobotModelSerializer(instance=obj.robot_monitor).data
