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
    @mock.patch('sentry_sdk.Client', autospec=True)
    @mock.patch('sentry_sdk.Scope', autospec=True)
    @mock.patch('sentry_sdk.Hub', autospec=True)
    def test_init(self, mock_hub, mock_scope, mock_client):

        kuyruk_sentry.Sentry(k)

        assert mock_client.called
        assert mock_scope.called
        assert mock_hub.called

    @mock.patch('sentry_sdk.Client', autospec=True)
    @mock.patch.object(sentry_sdk.Hub, 'capture_exception', autospec=True)
    def test_save_exception(self, mock_capture_exception, mock_client):

        kuyruk_sentry.Sentry(k)

        queues = "kuyruk"
        args, kwargs = (), {}
        desc = error._get_description(args, kwargs)

        message = mock.Mock(
            delivery_info={'routing_key': None},
            channel=mock.Mock()
        )
        w = kuyruk.Worker(k, Args(queues, False))
        w._process_task(message, desc, error, args, kwargs)

        assert mock_capture_exception.called
