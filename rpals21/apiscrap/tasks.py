from celery import Task, chord, current_app as app
from celery.worker.request import Request
from django.core.mail import EmailMessage
from django.utils import timezone
import ast
import os
import time

from apiscrap.models import TasksRobot, RobotMonitor
from utils.mydebugs import save_log_debug


class MyRequest(Request):
    def on_accepted(self, pid, time_accepted):
        """Handler called when task is accepted by worker pool."""
        super(MyRequest, self).on_accepted(pid, time_accepted)
        body = ast.literal_eval(self.body[1:(self.body.find('],') + 1)])  # Get body params

        robot_mon = RobotMonitor.objects.get(pk=int(body[0]))
        # TaskRobot Created
        TasksRobot.objects.create(
            task_celey_id=self.task_id,
            task_label=self.task_name,
            robot_monitor=robot_mon
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

    def __get_task_robot(self, task_celery_id):
        return TasksRobot.objects.get(task_celey_id=task_celery_id)

    #  Overrides Methods
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
        self.__get_task_robot(task_id).change_data(
            result=retval,
            finished=timezone.now()
        )

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
        self.__get_task_robot(task_id).change_data(
            exception=einfo,
            finished=timezone.now()
        )

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
        self.__get_task_robot(task_id).change_data(
            status=status
        )


@app.task(name='InitRobot')
def run_robots(pk=None):
    return chord(
        (add.s(pk, 5, 5), add.s(pk, 1, 4), add.s(pk), div.s(pk), saludar.s(pk), saludar.s(pk, 'Fredy Mendoza Vargas'))
    )(callback_result.s(pk).on_error(callback_result.s(pk)))


@app.task(bind=True, base=CustomTaskRobot, name='TaskSaludo')
def saludar(self, pk_robotmon, name='World'):
    print('Saludar pk <{}>'.format(pk_robotmon))
    time.sleep(60)
    return 'Hello {}, How are you?'.format(name)


@app.task(bind=True, base=CustomTaskRobot, name='AddTask')
def add(self, pk_robotmon, a=1, b=2):
    print('Sumando pK <{}>'.format(pk_robotmon))
    time.sleep(20)
    return a + b


@app.task(bind=True, base=CustomTaskRobot, name='DivTasks')
def div(self, pk_robotmon, a=1, b=0):
    print('Dividiendo pK <{}>'.format(pk_robotmon))
    time.sleep(5)
    return a / b


@app.task(name='ResultTask')
def callback_result(resp, pk):
    (generate_report.s() | send_email.s(pk))()


@app.task
def generate_report():
    dir_file = 'temps/report_user.xlsx'
    # workbook = xlsxwriter.Workbook(dir_file, {'remove_timezone': True, 'default_date_format': 'dd/mm/yy'})
    # worksheet = workbook.add_worksheet()
    #
    # # Add a bold format to use to highlight cells.
    # bold = workbook.add_format({'bold': 1})
    #
    # # Write some data headers.
    # for col in range(len(HEADERS)):
    #     worksheet.write(0, col, HEADERS[col], bold)
    #
    # users = User.objects.filter(is_active=1)
    # for row, user in enumerate(users, start=1):
    #     for col in range(len(HEADERS)):
    #         worksheet.write(row, col, user.__dict__[HEADERS[col]])
    #
    # workbook.close()
    return dir_file


@app.task
def send_email(filepath, pk):
    e = EmailMessage('Reportes', 'Cuerpo del mensaje {} con Pk {}'.format(filepath, pk),
                     to=['fredylsvprueba@gmail.com', 'fredymv03@gmail.com'])
    # e.attach_file(filepath)  # Adjuntamos el archivo a enviar.
    e.send()

    return filepath


@app.task
def removefile(route):
    os.remove(route)
    return 'Archivo borrado!!'
