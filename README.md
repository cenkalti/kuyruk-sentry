# Kuyruk-Sentry

Sends exceptions in Kuyruk workers to Sentry.

## Install

    $ pip install kuyruk-sentry

## Usage

```python
from kuyruk import Kuyruk, Config
from kuyruk_sentry import Sentry

config = Config()
config.KUYRUK_SENTRY_DSN = "..."

kuyruk = kuyruk.Kuyruk(config)

s = Sentry(k)

@kuyruk.task
def oops():
    1/0  # exception will be sent to Sentry
```