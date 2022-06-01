# retry
## Exception type based retry decorator for all your problematic functions.


Inspired by: https://wiki.python.org/moin/PythonDecoratorLibrary#Retry


    # Parmeters

    Exceptions:
        description: Exception(s) to check. May be a tuple of exceptions to check.
        example: IOError or IOError(errno.ECOMM) or (IOError,) or (ValueError, IOError(errno.ECOMM)
        type: Exception type, exception instance, or tuple containing any number of both

    Tries:
        description: Number of times to try (not retry) before giving up.
        example: 3
        type: integer

    Delay:
        description: Initial delay between retries in seconds.
        example: 3
        type: integer

    Backoff:
        description: Backoff multiplier
        example: Value of 2 will double the delay each retry
        type: integer

    Silent:
        description: If set then no logging will be attempted.
        example: True
        type: Boolean

    Logger:
        description: Logger to use. If None, print.
        example: log = getLogger(__name__)
        type: logging.Logger


## Usage

```python
from logging import basicConfig, getLogger, INFO
from retry import retry

basicConfig(level=INFO)
log = getLogger(__name__)

@retry((TestError, IOError), tries=6, delay=1, backoff=2, silent=False, logger=log)
def yourfunction(self, example):
    try:
        ...
    except:
        raise TestError
    finally:
        log.INFO('No Errors!')
```


## Examples

### Always Fail

```python
from retry import retry

@retry(Exception, tries=4)
def test_fail(text):
    raise Exception('Fail')

test_fail('It Works!')
```

### Success

```python
from retry import retry

@retry(Exception, tries=4)
def test_success(text):
    print('Success: {0}'.format(text))

test_success('It Works!')
```

### Random Fail

```python
from retry import retry
from random import random

@retry(Exception, tries=4)
def test_random(text):
    x = random()
    if x < 0.5:
        raise Exception('Fail')
    else:
        print('Success: {0}'.format(text))

test_random('It Works!')
```

### Handling Multiple Exceptions

```python
from retry import retry
from random import random

@retry((NameError, IOError), tries=20, delay=1, backoff=1)
def test_multiple_exceptions():
    x = random()
    if x < 0.40:
        raise NameError('NameError')
    elif x < 0.80:
        raise IOError('IOError')
    else:
        raise KeyError('KeyError')

test_multiple_exceptions()
```
