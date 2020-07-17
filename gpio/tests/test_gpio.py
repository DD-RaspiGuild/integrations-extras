import mock

from datadog_checks.base import AgentCheck
from datadog_checks.gpio import GpioCheck
from datadog_checks.base.errors import CheckException
from datadog_checks.dev.utils import get_metadata_metrics

def mock_exec_readall():
    return """ +-----+-----+---------+------+---+---Pi 3B--+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 0 |  7 || 8  | 0 | IN   | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | IN   | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 0 | 11 || 12 | 1 | OUT  | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 1 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | IN   | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 3B--+---+------+---------+-----+-----+"""

# def test_empty_check(empty_instance):
#     check = GpioCheck("gpio", {}, {})

#     with pytest.raises(CheckException):
#         check.check(empty_instance)

def test_valid_check(aggregator, instance):
    check = GpioCheck("gpio", {}, {})

    with mock.patch.object(check, "execute_gpio_readall", return_value=mock_exec_readall()):
        check.check(instance)
    aggregator.assert_metric("gpio.SDA.1", value=1)
    aggregator.assert_metric("gpio.SCL.1", value=1)
    aggregator.assert_metric("gpio.GPIO.7", value=0)
    aggregator.assert_metric("gpio.GPIO.0", value=0)
    aggregator.assert_metric("gpio.GPIO.2", value=0)
    aggregator.assert_metric("gpio.GPIO.3", value=0)
    aggregator.assert_metric("gpio.MOSI", value=0)
    aggregator.assert_metric("gpio.MISO", value=0)
    aggregator.assert_metric("gpio.SCLK", value=0)
    aggregator.assert_metric("gpio.SDA.0", value=1)
    aggregator.assert_metric("gpio.GPIO.21", value=1)
    aggregator.assert_metric("gpio.GPIO.22", value=1)
    aggregator.assert_metric("gpio.GPIO.23", value=0)
    aggregator.assert_metric("gpio.GPIO.24", value=0)
    aggregator.assert_metric("gpio.GPIO.25", value=0)
    aggregator.assert_metric("gpio.TxD", value=0)
    aggregator.assert_metric("gpio.RxD", value=1)
    aggregator.assert_metric("gpio.GPIO.1", value=1)
    aggregator.assert_metric("gpio.GPIO.4", value=0)
    aggregator.assert_metric("gpio.GPIO.5", value=0)
    aggregator.assert_metric("gpio.GPIO.6", value=0)
    aggregator.assert_metric("gpio.CE0", value=1)
    aggregator.assert_metric("gpio.CE1", value=1)
    aggregator.assert_metric("gpio.SCL.0", value=1)
    aggregator.assert_metric("gpio.GPIO.26", value=0)
    aggregator.assert_metric("gpio.GPIO.27", value=0)
    aggregator.assert_metric("gpio.GPIO.28", value=0)
    aggregator.assert_metric("gpio.GPIO.29", value=0)
    aggregator.assert_all_metrics_covered()
