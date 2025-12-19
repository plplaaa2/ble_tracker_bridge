from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: ConfigType):
    """No YAML support."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Initialize entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "data": entry.data,
        "options": entry.options,
    }

    # Reload when options change (e.g., sensors modified)
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    # Forward to device_tracker platform
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["device_tracker"])
    )

    return True

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options updates by reloading the entry."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unloads(entry, ["device_tracker"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
