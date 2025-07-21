import time

import pytest

from retry import retry


class UserDefinedException(Exception):
    pass


def test_retry(monkeypatch):
    mock_sleep_time = [0]

    def mock_sleep(seconds):
        mock_sleep_time[0] += seconds

    monkeypatch.setattr(time, "sleep", mock_sleep)

    hit = [0]

    tries = 5
    delay = 1
    backoff = 2

    @retry(tries=tries, delay=delay, backoff=backoff)
    def f():
        hit[0] += 1
        raise UserDefinedException("...")

    with pytest.raises(UserDefinedException):
        f()
    assert hit[0] == tries
    assert mock_sleep_time[0] == sum(delay * backoff**i for i in range(tries - 1))


def test_retry_function_with_args(monkeypatch):
    mock_sleep_time = [0]

    def mock_sleep(seconds):
        mock_sleep_time[0] += seconds

    monkeypatch.setattr(time, "sleep", mock_sleep)

    hit = [0]

    tries = 5
    delay = 1
    backoff = 2

    @retry(tries=tries, delay=delay, backoff=backoff)
    def f(msg: str):
        hit[0] += 1
        raise UserDefinedException(msg)

    with pytest.raises(UserDefinedException):
        f("Hello")
    assert hit[0] == tries
    assert mock_sleep_time[0] == sum(delay * backoff**i for i in range(tries - 1))


def test_retry_function_with_kwargs(monkeypatch):
    mock_sleep_time = [0]

    def mock_sleep(seconds):
        mock_sleep_time[0] += seconds

    monkeypatch.setattr(time, "sleep", mock_sleep)

    hit = [0]

    tries = 5
    delay = 1
    backoff = 2

    @retry(tries=tries, delay=delay, backoff=backoff)
    def f(msg: str):
        hit[0] += 1
        raise UserDefinedException(msg)

    with pytest.raises(UserDefinedException):
        f(msg="Hello")
    assert hit[0] == tries
    assert mock_sleep_time[0] == sum(delay * backoff**i for i in range(tries - 1))


def test_tries_minus1():
    hit = [0]
    target = 10

    @retry(tries=-1)
    def f():
        hit[0] += 1
        if hit[0] == target:
            return target
        else:
            raise ValueError

    assert f() == target


def test_max_delay(monkeypatch):
    mock_sleep_time = [0]

    def mock_sleep(seconds):
        mock_sleep_time[0] += seconds

    monkeypatch.setattr(time, "sleep", mock_sleep)

    hit = [0]

    tries = 5
    delay = 1
    backoff = 2
    max_delay = delay  # Never increase delay

    @retry(tries=tries, delay=delay, max_delay=max_delay, backoff=backoff)
    def f():
        hit[0] += 1
        raise UserDefinedException("...")

    with pytest.raises(UserDefinedException):
        f()
    assert hit[0] == tries
    assert mock_sleep_time[0] == delay * (tries - 1)


def test_fixed_jitter(monkeypatch):
    mock_sleep_time = [0]

    def mock_sleep(seconds):
        mock_sleep_time[0] += seconds

    monkeypatch.setattr(time, "sleep", mock_sleep)

    hit = [0]

    tries = 10
    jitter = 1

    @retry(tries=tries, jitter=jitter)
    def f():
        hit[0] += 1
        raise UserDefinedException("...")

    with pytest.raises(UserDefinedException):
        f()
    assert hit[0] == tries
    assert mock_sleep_time[0] == sum(range(tries - 1))
