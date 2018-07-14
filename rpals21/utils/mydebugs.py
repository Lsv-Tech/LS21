import datetime
import os
from django.conf import settings

LOG_DIR = os.path.join(settings.BASE_DIR, 'debugtask')


def save_log_debug(msg):
    """Funcion que guarda un log de los errores tomados del Celery Request """
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    with open(LOG_DIR + '/logs.txt', 'a') as file:
        file.write('[date]: "{}" - [msg]: "{}" \n'.format(datetime.datetime.now(), msg))
