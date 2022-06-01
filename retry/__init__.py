from functools import wraps
from time import sleep

def retry(exceptions, tries=4, delay=3, backoff=2, silent=False, logger=None):
    try:
        len(exceptions)
    except TypeError:
        exceptions = (exceptions,)
    all_exception_types = tuple(set(x if type(x) == type else x.__class__
                                    for x in exceptions))
    exception_types = tuple(x for x in exceptions if type(x) == type)
    exception_instances = tuple(x for x in exceptions if type(x) != type)

    def wrapper(f):
        if tries in (None, 0):
            message = 'Retry: [DISABLED]'
            if not silent:
                if logger:
                    logger.debug(message)
                else:
                    print(message)

            return f

        @wraps(f)
        def _retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except all_exception_types as e:
                    if (not any(x for x in exception_types
                                if isinstance(e, x)) and
                        not any(x for x in exception_instances
                                if type(x) == type(e) and
                                x.args == e.args)):
                        raise
                    msg = (f'Retry ({mtries:d}/{tries:d}):\n'
                           f'{str(e) if str(e) != "" else repr(e)}\n'
                           f'Retrying in {mdelay} second(s)...')
                    if not silent:
                        if logger:
                            logger.warning(msg)
                        else:
                            print(msg)
                    sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff

            return f(*args, **kwargs)

        return _retry

    return wrapper
