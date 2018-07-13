from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from .models import RobotMonitor, TasksRobot
from .serializers import RobotModelSerializer, TaskRobotModelSerializer
from .tasks import run_robots


class RobotModelViewSet(ModelViewSet):
    queryset = RobotMonitor.objects.all()
    serializer_class = RobotModelSerializer

    def list(self, request, *args, **kwargs):
        run_robots.delay(4)
        return super(RobotModelViewSet, self).list(request, *args, **kwargs)


class TaskRobotModelViewSet(ModelViewSet):
    queryset = TasksRobot.objects.all()
    serializer_class = TaskRobotModelSerializer

    # def perform_create(self, serializer):
    #     robot = serializer.save()
    #     run_robots.delay(robot)
