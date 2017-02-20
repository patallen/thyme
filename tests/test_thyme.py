from thyme.thyme import Thyme
from thyme.modes import DatetimeMode, TimestampMode


def test_thyme_init():
    thyme = Thyme({'datetime': True})
    assert len(thyme._kwargs)


def test_thyme__get_mode():
    dt = Thyme({'date': True})
    assert dt._get_mode(dt._kwargs) == DatetimeMode

    stamp = Thyme({'stamp': True})
    assert stamp._get_mode(stamp._kwargs) == TimestampMode


def test_thyme_run():
    thyme = Thyme({'date': True})

    assert thyme.run() is None
