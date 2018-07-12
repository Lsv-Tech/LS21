from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Robot
from .tasks import initrobot


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RobotModelSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    owner_obj = serializers.SerializerMethodField()

    class Meta:
        model = Robot
        fields = ('id', 'started', 'finished', 'input_data', 'output_data', 'status', 'owner', 'owner_obj')

    def get_owner_obj(self, obj):
        return UserModelSerializer(obj.owner).data

    def save(self, **kwargs):
        # robot = super(RobotModelSerializer, self).save(**kwargs)
        initrobot.delay()
        # return robot
