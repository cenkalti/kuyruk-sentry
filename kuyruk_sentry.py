import raven
from kuyruk.events import task_failure


CONFIG_KEYS = ["SENTRY_DSN"]


class Sentry(object):

    def __init__(self, kuyruk):
        self.client = raven.Client(kuyruk.config.SENTRY_DSN)
        task_failure.connect(self.capture_exception, sender=kuyruk, weak=False)

    def capture_exception(self, sender, task, args, kwargs, exc_info):
        self.client.captureException(exc_info, extra={
            "task": task.name,
            "args": str(args),
            "kwargs": str(kwargs),
        })
