# Kuyruk-Sentry

Sends exceptions in Kuyruk workers to Sentry.

## Install

    $ pip install kuyruk-sentry

## Usage

```python
from kuyruk import Kuyruk, Config
from kuyruk_sentry import Sentry
import sentry_sdk

sentry_sdk.init(dsn="...")  # configure Sentry

config = Config()
kuyruk = Kuyruk(config)

s = Sentry(kuyruk)

@kuyruk.task
def oops():
    1/0  # exception will be sent to Sentry
```
