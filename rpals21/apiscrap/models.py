from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class RobotMonitor(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('ON_GOING', 'On Going'),
        ('STOPPED', 'Stopped'),
        ('FINISHED', 'Finished')
    )

    search_key = models.CharField(max_length=200)
    started = models.DateTimeField(auto_now_add=True, auto_now=False)
    finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CREATED')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='robots')

    def __str__(self):
        return 'Robot #{} - By: {}.'.format(self.pk, self.owner.username)


class TasksRobot(models.Model):
    STATUS_TASK = (
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('FAILURE', 'Failure'),
        ('REVOKED', 'Revoked'),
        ('SUCCESS', 'Success')
    )
    robot_monitor = models.ForeignKey(RobotMonitor, on_delete=models.CASCADE, related_name='tasks')
    task_celey_id = models.CharField(max_length=255)
    task_label = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    finished = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_TASK, default='STARTED')
    result = models.TextField(blank=True, null=True)
    exception = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.task_label if self.task_label else self.task_celey_id

    def change_data(self, **kwargs):
        self.__dict__.update(**kwargs)
        self.save()
