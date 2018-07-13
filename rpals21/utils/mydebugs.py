import datetime
import os
from django.conf import settings

LOG_DIR = os.path.join(settings.BASE_DIR, 'debugtask')


def save_log_debug(msg):
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    with open(LOG_DIR + '/logs.txt', 'a') as file:
        file.write('[date]: "{}" - [msg]: "{}" '.format(datetime.datetime.now(), msg))
