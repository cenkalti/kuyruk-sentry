import os
import sys
import socket
from datetime import datetime

import blinker
import raven
from kuyruk import signals


CONFIG = {"SENTRY_DSN": None}


class Sentry(object):

    def __init__(self, kuyruk):
        kuyruk.extensions["sentry"] = self
        self.client = raven.Client(kuyruk.config.SENTRY_DSN)
        self.on_exception = blinker.Signal()
        signals.worker_failure.connect(
            self.capture_exception, sender=kuyruk, weak=False)

    def capture_exception(self, sender, description, exc_info, worker, **extra):
        sentry_id = self.client.get_ident(self.client.captureException(exc_info, extra={
            "description": description,
            "worker_queues": worker.queues,
            "worker_hostname": socket.gethostname(),
            "worker_pid": os.getpid(),
            "worker_cmd": ' '.join(sys.argv),
            "worker_timestamp": datetime.utcnow().isoformat()[:19],
        }))
        description["sentry_id"] = sentry_id
        self.on_exception.send(sender, description=description,
                               exc_info=exc_info, worker=worker, **extra)
