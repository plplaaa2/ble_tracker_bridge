import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import DOMAIN, CONF_SENSORS

class BleTrackerBridgeConfigFlow(config_entries.ConfigFlow):
    """BLE Tracker Bridge config flow."""
    domain = DOMAIN
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="BLE Tracker Bridge", data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_SENSORS): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor", multiple=True)
            )
        })
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry):
        return BleTrackerBridgeOptionsFlowHandler(config_entry)


class BleTrackerBridgeOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        default_sensors = self.config_entry.options.get(CONF_SENSORS) or self.config_entry.data.get(CONF_SENSORS, [])
        schema = vol.Schema({
            vol.Required(CONF_SENSORS, default=default_sensors): selector.EntitySelector(
                selector.EntitySelectorConfig(domain="binary_sensor", multiple=True)
            )
        })
        return self.async_show_form(step_id="init", data_schema=schema)
