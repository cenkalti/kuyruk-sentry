import unittest
import unittest.mock
from collections import namedtuple

import kuyruk
import kuyruk_sentry
import sentry_sdk

c = kuyruk.Config()
k = kuyruk.Kuyruk(c)


@k.task()
def error():
    1/0


Args = namedtuple("Args", ["queues", "local", "logging_level",
                           "max_run_time", "max_load", "priority"])
Args.__new__.__defaults__ = (None,) * len(Args._fields)


class SentryTestCase(unittest.TestCase):
    @unittest.mock.patch('kuyruk_sentry.sentry_sdk.capture_exception')
    def test_save_exception(self, mock_capture_exception):
        kuyruk_sentry.Sentry(k)

        queues = "kuyruk"
        args, kwargs = (), {}
        desc = error._get_description(args, kwargs)

        message = unittest.mock.Mock(
            delivery_info={'routing_key': None},
            channel=unittest.mock.Mock()
        )
        w = kuyruk.Worker(k, Args(queues, False))
        w._process_task(message, desc, error, args, kwargs)

        mock_capture_exception.assert_called_once()

        mock_args = mock_capture_exception.call_args.args
        mock_kwargs = mock_capture_exception.call_args.kwargs

        (exc_type, exc, traceback) = mock_args[0]
        assert exc_type == ZeroDivisionError

        keys = {
            'description',
            'queue',
            'worker_hostname',
            'worker_pid',
            'worker_cmd',
            'worker_timestamp',
        }
        assert set(mock_kwargs['extras'].keys()) <= keys
