import logging
import voluptuous as vol
from homeassistant.components.notify import PLATFORM_SCHEMA, BaseNotificationService
import homeassistant.helpers.config_validation as cv
from signald import Signal

REQUIREMENTS = []
_LOGGER = logging.getLogger("signaldmessenger")

CONF_SENDER_NR = "sender_nr"
CONF_RECP_NR = "recp_nr"
CONF_GROUP = "group"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_SENDER_NR): cv.string,
        vol.Optional(CONF_RECP_NR): cv.string,
        vol.Optional(CONF_GROUP): cv.string,
    }
)


def get_service(hass, config, discovery_info=None):
    sender_nr = config.get(CONF_SENDER_NR)
    recp_nr = config.get(CONF_RECP_NR)
    group = config.get(CONF_GROUP)

    if not ((recp_nr is None) ^ (group is None)):
        _LOGGER.error("Either recp_nr or group is required")
        return False

    signal = Signal(sender_nr, socket_path="/signald/signald.sock")
    return SignaldNotificationService(signal, recp_nr, group)


class SignaldNotificationService(BaseNotificationService):
    def __init__(self, signal, recp_nr, group):
        self.signal = signal
        self.recp_nr = recp_nr
        self.group = group

    def send_message(self, message="", **kwargs):
        attachments = []
        if kwargs is not None:
            data = kwargs.get("data", None)
            if data is not None:
                attachments = data.get("attachments", [])
        if self.group is not None:
            self.signal.send_group_message(self.group, message, False, attachments)
        else:
            self.signal.send_message(self.recp_nr, message, False, attachments)
