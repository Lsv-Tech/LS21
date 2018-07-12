from celery import current_app as app, group, chord, Task
from celery.worker.request import Request
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

from apiscrap.models import MyTask
import time


class CustomRequest(Request):

    def on_accepted(self, pid, time_accepted):
        super(CustomRequest, self).on_accepted(pid, time_accepted)
        # Task accept going to save on database
        self.task.update_state(task_id=self.task_id, state='PENDING', meta={'info': 'waiting a free worker'})


class CustomTask(Task):
    Request = CustomRequest

    def update_state(self, task_id=None, state=None, meta=None):
        if task_id is None:
            task_id = self.request.id

        if state == 'STARTED' or state == 'PENDING':
            # print(f"Change state to => {state}")
            try:
                task_db = MyTask.objects.get(task_id=task_id)
                task_db.status = state
                task_db.save()
            except ObjectDoesNotExist:
                # If task don't exist on db will be create
                try:
                    MyTask.objects.create(task_id=task_id, status=state).save()
                except IntegrityError:
                    # Unique Constraint Error
                    pass
        else:
            print(task_id)
            # self.backend.store_result(task_id, meta, state)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if status == 'PAUSED':
            pass  # Save robot serialized when is PAUSED
        else:  # Clean on TaskRun database task totally executed
            try:
                task = MyTask.objects.get(task_id=task_id)
                task.status = 'SUCCESS'
                task.retval = retval
                task.save()
                # print(f"Task {task_id} deleted")
            except ObjectDoesNotExist:
                # print(f"Task {task_id} isn't enable to delete (Object Doesn't Exist)")
                pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # Delete task from task running table
        try:
            task = MyTask.objects.get(task_id=task_id)
            task.status = 'FAILED'
            task.save()
            # print(f"Task {task_id} deleted")
        except ObjectDoesNotExist:
            # print(f"Task {task_id} isn't enable to delete (Object Doesn't Exist)")
            pass


@app.task()
def initrobot():
    # job = group([
    #     sum.s(2, 2),
    #     mult.s(4, 4),
    #     sum.s(8, 8),
    #     mult.s(2, 1),
    #     sum.s(5, 5),
    # ])
    #
    # job.apply_async(link=lambda x: print(x))

    return chord(
        (sum.s(1, 1), mult.s(2, 2), div.s(2, 2))
    )(result.s().on_error(callback_error.s()))


@app.task(base=CustomTask, bind=True)
def sum(self, x, y):
    time.sleep(60)
    self.update_state(state='STARTED', meta={'msg': 'Working run'})
    return x + y


@app.task()
def callback_error(error, *args, **kwargs):
    print(args)
    print(kwargs)
    print('+' * 50)
    print(error)
    print(type(error))
    print('+' * 50)


@app.task(base=CustomTask, bind=True)
def mult(self, x, y):
    return x * y


@app.task(base=CustomTask, bind=True)
def div(self, x, y):
    return x / y
    # try:
    #     return x / y
    # except ZeroDivisionError:
    #     return -1


@app.task()
def result(result):
    print('*' * 50)
    print(result)
    print('*' * 50)

# c = chain(group(add.s(i, i) for i in range(1)) | xsum.s().on_error(on_chord_error.s())).delay()
