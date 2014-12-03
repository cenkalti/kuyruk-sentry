import unittest
from collections import namedtuple

import mock

import kuyruk
import kuyruk_sentry

c = kuyruk.Config()
c.SENTRY_DSN = "..."

k = kuyruk.Kuyruk(c)


@k.task
def error():
    1/0


Args = namedtuple("Args", ["queue", "local"])


class SentryTestCase(unittest.TestCase):

    @mock.patch("kuyruk_sentry.raven")
    def test_save_exception(self, mock_raven):
        s = kuyruk_sentry.Sentry(k)

        queue = "kuyruk"
        args, kwargs = (), {}
        desc = error._get_description(args, kwargs, queue)

        message = mock.Mock()
        w = kuyruk.Worker(k, Args(queue, False))
        w._process_task(message, desc, error, args, kwargs)

        assert s.client.captureException.called
