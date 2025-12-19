from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_SENSORS

class BleTrackerBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title="BLE Tracker Bridge",
                data={CONF_SENSORS: user_input.get(CONF_SENSORS, [])},
            )

        schema = vol.Schema({
            vol.Optional(CONF_SENSORS, default=[]): [str],
        })
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
