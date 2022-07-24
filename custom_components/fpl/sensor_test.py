"""Test Sensors"""
from datetime import timedelta, datetime
from homeassistant.components.sensor import (
    STATE_CLASS_TOTAL_INCREASING,
    DEVICE_CLASS_ENERGY,
)
from homeassistant.core import callback
from .fplEntity import FplEnergyEntity


class TestSensor(FplEnergyEntity):
    """Daily Usage Kwh Sensor"""

    def __init__(self, coordinator, config, account):
        super().__init__(coordinator, config, account, "Test Sensor")

    _attr_state_class = STATE_CLASS_TOTAL_INCREASING
    _attr_device_class = DEVICE_CLASS_ENERGY

    @property
    def native_value(self):
        data = self.getData("daily_usage")

        if data is not None and len(data) > 0 and "usage" in data[-1].keys():
            return data[-1]["usage"]

        return None

    @property
    def last_reset(self) -> datetime | None:
        data = self.getData("daily_usage")
        date = data[-1]["readTime"]
        last_reset = date - timedelta(days=1)
        return last_reset

    def customAttributes(self):
        """Return the state attributes."""
        data = self.getData("daily_usage")
        date = data[-1]["readTime"]

        attributes = {}
        attributes["date"] = date
        return attributes
