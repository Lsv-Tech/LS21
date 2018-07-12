from django.contrib import admin

# Register your models here.
from .models import Robot, MyTask


class MyTaskModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'task_id', 'status')

    class Meta:
        model = MyTask


admin.site.register(Robot)
admin.site.register(MyTask, MyTaskModelAdmin)
