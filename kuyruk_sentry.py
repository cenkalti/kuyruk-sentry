import os
import sys
import socket
from datetime import datetime

import blinker
import sentry_sdk
from kuyruk import signals

CONFIG = {"SENTRY_DSN": None}


class Sentry(object):
    def __init__(self, kuyruk):
        kuyruk.extensions["sentry"] = self
        scope = sentry_sdk.Scope()
        client = sentry_sdk.Client(kuyruk.config.SENTRY_DSN)
        self.hub = sentry_sdk.Hub(client, scope)
        self.on_exception = blinker.Signal()
        signals.worker_failure.connect(
            self.capture_exception, sender=kuyruk, weak=False)

    def capture_exception(self,
                          sender,
                          description=None,
                          exc_info=None,
                          worker=None,
                          queue=None,
                          **extra):
        with self.hub.push_scope() as scope:
            extras = {
                        "description": description,
                        "queue": queue,
                        "worker_hostname": socket.gethostname(),
                        "worker_pid": os.getpid(),
                        "worker_cmd": ' '.join(sys.argv),
                        "worker_timestamp": datetime.utcnow().isoformat()[:19],
                    }
            for key, value in extras.items():
                scope.set_extra(key, value)
            sentry_id = self.hub.capture_exception(exc_info)
        description["sentry_id"] = sentry_id
        self.on_exception.send(
            sender,
            description=description,
            exc_info=exc_info,
            worker=worker,
            queue=queue,
            **extra)
