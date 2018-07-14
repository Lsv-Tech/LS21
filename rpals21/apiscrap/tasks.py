from celery import Task, chord, current_app as app
from celery.worker.request import Request
from django.core.mail import EmailMessage
from django.utils import timezone
import ast
import json
import os
import xlsxwriter

from apiscrap.models import TasksRobot, RobotMonitor
from utils.constans import HEADERS
from utils.mercadolibre.main import Scrap

from utils.mydebugs import save_log_debug


class MyRequest(Request):
    def on_accepted(self, pid, time_accepted):
        """Handler called when task is accepted by worker pool."""
        super(MyRequest, self).on_accepted(pid, time_accepted)
        body = ast.literal_eval(self.body[1:(self.body.find('],') + 1)])  # Get body params pk
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
        save_log_debug('Failure detected for task {}: Hard time limit ({}s) exceeded for {}[{}]'.format(
            self.task, timeout, self.name, self.id))

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        """Handler called if the task raised an exception."""
        super(MyRequest, self).on_failure(exc_info, send_failed_event, return_ok)
        # Save debug Exceptio From Request
        save_log_debug('Failure detected for task'.format(self.task.name))


class CustomTaskRobot(Task):
    Request = MyRequest

    def __get_task_robot(self, task_celery_id):
        return TasksRobot.objects.get(task_celey_id=task_celery_id)

    #  Overrides Methods
    def on_success(self, retval, task_id, args, kwargs):
        """Success handler."""
        self.__get_task_robot(task_id).change_data(
            result=retval,
            finished=timezone.now()
        )

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Retry handler."""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Error handler."""
        self.__get_task_robot(task_id).change_data(
            exception=einfo,
            finished=timezone.now()
        )

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Handler called after the task returns."""
        self.__get_task_robot(task_id).change_data(
            status=status
        )


@app.task(name='InitRobot')
def run_robots(pk=None, search='Zapatos'):
    return chord(
        (mercadolibre.s(pk, search), mercadolibre.s(pk, 'Celular Nokia 5 Azul Con Pantalla 5.2'))
    )(callback_result.s(pk).on_error(callback_result.s(pk)))


@app.task(bind=True, base=CustomTaskRobot, name='TaskMercadoLibre')
def mercadolibre(self, pk, search):
    scrap = Scrap()
    scrap.generar_articulos(search)
    return json.dumps(scrap.l_articulos)


@app.task(name='ResultTask')
def callback_result(resp, pk):
    RobotMonitor.objects.get(pk=pk).change_data(status='FINISHED', finished=timezone.now())
    (generate_report.s(pk) | send_email.s(pk) | removefile.s())()


@app.task
def generate_report(pk):
    dir_file = 'report.xlsx'
    rob = RobotMonitor.objects.get(pk=pk)
    workbook = xlsxwriter.Workbook(dir_file)
    bold = workbook.add_format({'bold': 1})

    for task in rob.tasks.all():
        if task.result:
            worksheet = workbook.add_worksheet(name='Task #{}'.format(str(task.id)))
            # Add a bold format to use to highlight cells.

            # Write some data headers.
            for col in range(len(HEADERS)):
                worksheet.write(0, col, HEADERS[col], bold)

            for row, art in enumerate(json.loads(task.result), start=1):
                for col in range(len(HEADERS)):
                    worksheet.write(row, col, art[HEADERS[col]])

    workbook.close()
    return dir_file


@app.task
def send_email(filepath, pk):
    robot = RobotMonitor.objects.get(pk=pk)
    task_fails = robot.tasks.filter(status='FAILURE').count()
    task_ok = robot.tasks.filter(status='SUCCESS').count()
    subject = 'ROBOT #{} FINALIZADO'
    msg = 'El robot #{} con la keyword -> {}:\n\nTareas Fallidas: {}\nTareas Finalizadas Corectamente: {}'.format(
        robot.id, robot.search_key, task_fails, task_ok)
    e = EmailMessage(subject, msg, to=['fredylsvprueba@gmail.com', 'fredymv03@gmail.com'])
    e.attach_file(filepath)  # Adjuntamos el archivo a enviar.
    e.send()
    return filepath


@app.task
def removefile(route):
    os.remove(route)
    return 'Archivo borrado!!'
