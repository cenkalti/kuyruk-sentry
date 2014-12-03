import os
import sys
import socket
from datetime import datetime

import raven
from kuyruk import signals


CONFIG = {"SENTRY_DSN": None}


class Sentry(object):

    def __init__(self, kuyruk):
        self.client = raven.Client(kuyruk.config.SENTRY_DSN)
        signals.worker_failure.connect(
            self.capture_exception, sender=kuyruk, weak=False)

    def capture_exception(self, sender, description, exc_info, worker, **extra):
        self.client.captureException(exc_info, extra={
            "description": description,
            "worker_queue": worker.queue,
            "worker_hostname": socket.gethostname(),
            "worker_pid": os.getpid(),
            "worker_cmd": ' '.join(sys.argv),
            "worker_timestamp": datetime.utcnow().isoformat()[:19],
        })
