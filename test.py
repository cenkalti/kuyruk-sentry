import unittest
from collections import namedtuple

import mock

import kuyruk
import kuyruk_sentry
import sentry_sdk

c = kuyruk.Config()
c.SENTRY_DSN = "..."

k = kuyruk.Kuyruk(c)


@k.task()
def error():
    1/0


Args = namedtuple("Args", ["queues", "local", "logging_level",
                           "max_run_time", "max_load"])
Args.__new__.__defaults__ = (None,) * len(Args._fields)


class SentryTestCase(unittest.TestCase):
    def test_init(self):
        sentry_sdk.init = mock.Mock()
        try:
            kuyruk_sentry.Sentry(k)
        except sentry_sdk.utils.BadDsn:
            pass

        assert sentry_sdk.init.called

    def test_save_exception(self):
        sentry_sdk.capture_exception = mock.Mock()

        try:
            kuyruk_sentry.Sentry(k)
        except sentry_sdk.utils.BadDsn:
            pass

        queues = "kuyruk"
        args, kwargs = (), {}
        desc = error._get_description(args, kwargs)

        message = mock.Mock(
            delivery_info={'routing_key': None},
            channel=mock.Mock()
        )
        w = kuyruk.Worker(k, Args(queues, False))
        w._process_task(message, desc, error, args, kwargs)

        assert sentry_sdk.capture_exception.called
