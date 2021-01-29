import logging
import voluptuous as vol
from homeassistant.components.notify import ATTR_DATA, PLATFORM_SCHEMA, BaseNotificationService
import homeassistant.helpers.config_validation as cv
from signald import Signal

REQUIREMENTS = []
_LOGGER = logging.getLogger(__name__)

CONF_SENDER_NR = "sender_nr"
CONF_RECP_NR = "recp_nr"
CONF_GROUP = "group"
CONF_SOCKET = "socket"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_SENDER_NR): cv.string,
        vol.Optional(CONF_RECP_NR): cv.string,
        vol.Optional(CONF_GROUP): cv.string,
        vol.Optional(CONF_SOCKET): cv.string,
    }
)


def get_service(hass, config, discovery_info=None):
    sender_nr = config.get(CONF_SENDER_NR)
    recp_nr = config.get(CONF_RECP_NR)
    group = config.get(CONF_GROUP)
    socket = config.get(CONF_SOCKET) or "/signald/signald.sock"

    if sender_nr is None:
        _LOGGER.error("sender_nr is required")
        return None
    if (recp_nr is None) and (group is None):
        _LOGGER.error("Either recp_nr or group is required")
        return None

    signal = Signal(sender_nr, socket_path=socket)
    return SignaldNotificationService(signal, recp_nr, group)


class SignaldNotificationService(BaseNotificationService):
    def __init__(self, signal, recp_nr, group):
        self._signal = signal
        self._recp_nr = recp_nr
        self._group = group

    def send_message(self, message="", **kwargs):
        data = (kwargs or {}).get("data") or {}
        attachments = data.get("attachments") or []
        if self._group is not None:
            self._signal.send_group_message(self._group, message, False, attachments)
        else:
            self._signal.send_message(self._recp_nr, message, False, attachments)
