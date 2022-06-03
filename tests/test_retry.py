import pytest

from logging import DEBUG, getLogger, StreamHandler
from retry import retry
from unittest import main, TestCase


class RetryableError(Exception):
    pass


class AnotherRetryableError(Exception):
    pass


class UnexpectedError(Exception):
    pass


class RetryTestCase(TestCase):
    def test_no_retry_required(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def succeeds():
            self.counter += 1
            return 'success'

        r = succeeds()

        assert r == 'success'
        assert self.counter == 1

    def test_retries_once(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def fails_once():
            self.counter += 1
            if self.counter < 2:
                raise RetryableError('failed')
            else:
                return 'success'

        r = fails_once()

        assert r == 'success'
        assert self.counter == 2

    def test_limit_is_reached(self):
        self.counter = 0

        @retry(RetryableError, tries=4, delay=0.1)
        def always_fails():
            self.counter += 1
            raise RetryableError('failed')

        with self.assertRaises(RetryableError):
            always_fails()

        assert self.counter == 4

    def test_multiple_exception_types(self):
        self.counter = 0

        @retry((RetryableError, AnotherRetryableError), tries=4, delay=0.1)
        def raise_multiple_exceptions():
            self.counter += 1
            if self.counter == 1:
                raise RetryableError('a retryable error')
            elif self.counter == 2:
                raise AnotherRetryableError('another retryable error')
            else:
                return 'success'

        r = raise_multiple_exceptions()

        assert r == 'success'
        assert self.counter == 3

    def test_unexpected_exception_does_not_retry(self):

        @retry(RetryableError, tries=4, delay=0.1)
        def raise_unexpected_error():
            raise UnexpectedError('unexpected error')

        with pytest.raises(UnexpectedError, match='unexpected error'):
            raise_unexpected_error()

    def test_using_a_logger(self):
        expected = {'DEBUG': 'success',
                    'ERROR': 'failed',
                    'WARNING': ('Retry (4/4):\nfailed\nRetrying in 0.1 '
                                'second(s)...')}
        records = {}
        self.counter = 0

        sh = StreamHandler()
        log = getLogger(__name__)
        log.addHandler(sh)

        @pytest.fixture(autouse=True)
        @retry(RetryableError, tries=4, delay=0.1, logger=log)
        def fails_once():
            self._caplog = caplog
            self._caplog.set_level(DEBUG)
            self.counter += 1
            if self.counter < 2:
                log.error('failed')
                raise RetryableError('failed')
            else:
                log.debug('success')
                for record in self._caplog.records:
                    records[record.levelname] = record.message
                return 'success'

        r = fails_once()

        assert r == 'success'
        assert self.counter == 2
        assert expected == records


if __name__ == '__main__':
    main()
