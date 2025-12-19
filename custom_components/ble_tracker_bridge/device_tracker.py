from __future__ import annotations
from typing import List

from homeassistant.components.device_tracker import SOURCE_TYPE_BLUETOOTH, ScannerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, CONF_SENSORS

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    sensors: List[str] = entry.options.get(CONF_SENSORS) or entry.data.get(CONF_SENSORS) or []
    entities = [BinarySensorPresenceTracker(hass, entry, sensor_id) for sensor_id in sensors]
    async_add_entities(entities, update_before_add=True)

class BinarySensorPresenceTracker(ScannerEntity):
    """Expose a binary_sensor presence as a device_tracker."""

    _attr_should_poll = False
    _attr_source_type = SOURCE_TYPE_BLUETOOTH

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, sensor_entity_id: str) -> None:
        self._hass = hass
        self._entry = entry
        self._sensor_entity_id = sensor_entity_id
        self._attr_name = f"{sensor_entity_id} tracker"
        self._attr_unique_id = f"{entry.entry_id}:{sensor_entity_id}"
        self._connected = False
        self._unsub_state = None
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="BLE Tracker Bridge",
            manufacturer="Custom",
            model="BinarySensor→DeviceTracker",
        )

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def async_added_to_hass(self) -> None:
        initial = self._hass.states.get(self._sensor_entity_id)
        self._connected = bool(initial and initial.state == "on")
        self.async_write_ha_state()
        self._unsub_state = async_track_state_change_event(
            self._hass, [self._sensor_entity_id], self._handle_sensor_change
        )

    async def async_will_remove_from_hass(self) -> None:
        if self._unsub_state:
            self._unsub_state()
            self._unsub_state = None

    @callback
    def _handle_sensor_change(self, event) -> None:
        new_state = event.data.get("new_state")
        if not new_state:
            return
        self._connected = new_state.state == "on"
        self.async_write_ha_state()
