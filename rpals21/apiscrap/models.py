from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Robot(models.Model):
    STATUS_CHOICES = (
        ('CREATED', 'Created'),
        ('ON_GOING', 'On Going'),
        ('ERROR', 'Error'),
        ('FINISHED', 'Finished')
    )

    started = models.DateTimeField(auto_now=True)
    finished = models.DateTimeField(null=True, blank=True)
    input_data = models.TextField()
    output_data = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='CREATED')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='robots')

    def __str__(self):
        return 'Robot #{} - By: {}.'.format(self.pk, self.owner.username)

    def change_status(self, status):
        self.status = status
        self.save()

    def finish(self, output):
        self.finished = timezone.now()
        self.status = 'FINISHED'
        self.output_data = output

        self.save()


class MyTask(models.Model):
    task_id = models.CharField(max_length=200)
    retval = models.TextField()
    status = models.CharField(max_length=100)
