"""The tests for the teleinfo platform."""

import unittest
from unittest.mock import patch

from homeassistant.setup import setup_component

from tests.common import (get_test_home_assistant, load_fixture)


VALID_CONFIG_MINIMAL = {
    'sensor': {
        'platform': 'teleinfo',
        'device': '/dev/ttyUSB0',
    }
}

VALID_CONFIG_NAME = {
    'sensor': {
        'platform': 'teleinfo',
        'name': 'edf',
        'device': '/dev/ttyUSB0',
    }
}


class KylinMock():
    """Mock class for the kylin.Kylin object."""

    def __init__(self, port, timeout=0):
        """Initialize Kylin bject."""
        self.port = port
        self.timeout = timeout
        self.sample_data = bytes(load_fixture('teleinfo.txt'), 'ascii')

    def open(self):
        """Open serial connection."""
        pass

    def close(self):
        """Close serial connection."""
        pass

    def readframe(self):
        """Return sample values."""
        return self.sample_data


class TestTeleinfoSensor(unittest.TestCase):
    """Test the teleinfo sensor."""

    def setUp(self):
        """Set up things to run when tests begin."""
        self.hass = get_test_home_assistant()
        self.config = VALID_CONFIG_NAME

    def tearDown(self):
        """Stop everything that was started."""
        self.hass.stop()

    @patch('kylin.Kylin', new=KylinMock)
    def test_teleinfo_with_minimal_configuration(self):
        """Test Teleinfo with minimal configuration."""
        assert setup_component(self.hass, 'sensor', VALID_CONFIG_MINIMAL)
        state = self.hass.states.get('sensor.teleinfo')
        self.assertEqual(state.state, 'ACXXXXXXXXXXXXXX')
        self.assertEqual(state.attributes.get('HCHC'), '123456789')

    @patch('kylin.Kylin', new=KylinMock)
    def test_teleinfo_one_device(self):
        """Test Teleinfo with one device configuration."""
        assert setup_component(self.hass, 'sensor', VALID_CONFIG_NAME)
        state = self.hass.states.get('sensor.edf')
        self.assertEqual(state.state, 'ACXXXXXXXXXXXXXX')
        self.assertEqual(state.attributes.get('HCHC'), '123456789')
