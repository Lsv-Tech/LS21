import ast, time
from celery import Task, chord, current_app as app
from celery.worker.request import Request

from apiscrap.models import TasksRobot, RobotMonitor
from utils.mydebugs import save_log_debug


class MyRequest(Request):
    def on_accepted(self, pid, time_accepted):
        """Handler called when task is accepted by worker pool."""
        print('on_accepted')
        super(MyRequest, self).on_accepted(pid, time_accepted)

        body = ast.literal_eval(self.body[1:(self.body.find('],') + 1)])  # Get body params
        print('hola')
        robot_mon = RobotMonitor.objects.get(int(body[0]))
        # TaskRobot Created
        TasksRobot.objects.create(
            task_celey_id=self.task_id,
            task_label=self.task_name,
            robot_mon=robot_mon
        )


def on_timeout(self, soft, timeout):
    """Handler called if the task times out."""
    super(MyRequest, self).on_timeout(soft, timeout)
    # save debug
    save_log_debug('Failure detected for task %s: Hard time limit (%ss) exceeded for %s[%s]',
                   self.task, timeout, self.name, self.id)


def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
    """Handler called if the task raised an exception."""
    super(MyRequest, self).on_failure(exc_info, send_failed_event, return_ok)
    # Save debug Exceptio From Request
    save_log_debug('Failure detected for task %s', self.task.name)


class CustomTaskRobot(Task):
    Request = MyRequest

    #  Overrides Methods

    def update_state(self, task_id=None, state=None, meta=None):
        """Update task state.

        Arguments:
            task_id (str): Id of the task to update.
                Defaults to the id of the current task.
            state (str): New state.
            meta (Dict): State meta-data.
        """
        if task_id is None:
            task_id = self.request.id
        # self.backend.store_result(task_id, meta, state)

    def on_success(self, retval, task_id, args, kwargs):
        """Success handler.

        Run by the worker if the task executes successfully.

        Arguments:
            retval (Any): The return value of the task.
            task_id (str): Unique id of the executed task.
            args (Tuple): Original arguments for the executed task.
            kwargs (Dict): Original keyword arguments for the executed task.

        Returns:
            None: The return value of this handler is ignored.
        """

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Retry handler.

        This is run by the worker when the task is to be retried.

        Arguments:
            exc (Exception): The exception sent to :meth:`retry`.
            task_id (str): Unique id of the retried task.
            args (Tuple): Original arguments for the retried task.
            kwargs (Dict): Original keyword arguments for the retried task.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.

        Returns:
            None: The return value of this handler is ignored.
        """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error handler.

        This is run by the worker when the task fails.

        Arguments:
            exc (Exception): The exception raised by the task.
            task_id (str): Unique id of the failed task.
            args (Tuple): Original arguments for the task that failed.
            kwargs (Dict): Original keyword arguments for the task that failed.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.

        Returns:
            None: The return value of this handler is ignored.
        """

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Handler called after the task returns.

        Arguments:
            status (str): Current task state.
            retval (Any): Task return value/exception.
            task_id (str): Unique id of the task.
            args (Tuple): Original arguments for the task.
            kwargs (Dict): Original keyword arguments for the task.
            einfo (~billiard.einfo.ExceptionInfo): Exception information.

        Returns:
            None: The return value of this handler is ignored.
        """


@app.task()
def run_robots(pk=None):
    print('AQUIII')
    print(pk)
    return chord(
        (add.s(pk, 5, 5), add.s(pk, 1, 4), add.s(pk), saludar(pk), saludar(pk, 'Fredy Mendoza Vargas'))
    )(callback_result.s())


@app.task(base=CustomTaskRobot, name='TaskSaludo')
def saludar(pk_robotmon=None, name='World'):
    print('pk <{}>'.format(pk_robotmon))
    time.sleep(60)
    return 'Hello {}, How are you?'.format(name)


@app.task(base=CustomTaskRobot, name='AddTask')
def add(pk_robotmon=None, a=1, b=2):
    time.sleep(20)
    print('pK <{}>'.format(pk_robotmon))
    return a + b


@app.task()
def callback_result(resp):
    print(resp)

# [["Fredy", "Mendoza"], {}, {"errbacks": null, "callbacks": null, "chain": null, "chord": null}]
# print(self.body)
# print(ast.literal_eval(self.body[1:(self.body.find('],') + 1)])[0])

# for item in fruits:
#     print(item)
