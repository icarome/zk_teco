from homeassistant.components.lock import SUPPORT_OPEN, LockDevice, PLATFORM_SCHEMA
from homeassistant.const import STATE_LOCKED, STATE_UNLOCKED
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import logging
from zk import ZK
import time
import homeassistant.util.dt as dt_util
_LOGGER = logging.getLogger(__name__)

CONF_PROTOCOL = "protocol"
CONF_PASSWORD= "password"
CONF_HOST = "host"
CONF_UNLOCK_TIMEOUT = "lock_timeout"
CONF_NAME = "name"
DEFAULT_NAME = "Door"
DEFAULT_HOST = "192.168.0.202"
DEFAULT_STATE = STATE_LOCKED
DEFAULT_PASSWORD = "12345"
DEFAULT_UNLOCK_TIMEOUT = 15
DEFAULT_PROTOCOL = "udp"
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Required(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
        vol.Required(CONF_PROTOCOL, default=DEFAULT_PROTOCOL): vol.In(["tcp", "udp"]),
        vol.Optional(CONF_UNLOCK_TIMEOUT, default=DEFAULT_UNLOCK_TIMEOUT): cv.positive_int,
    }
)
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Demo lock platform."""
    host = config.get(CONF_HOST)
    name = config.get(CONF_NAME)
    password = config.get(CONF_PASSWORD)
    if config.get(CONF_PROTOCOL) == "udp":
        force_udp = True
    else:
        force_udp = False
    unlock_timeout = config.get(CONF_UNLOCK_TIMEOUT)
    async_add_entities(
        [
            DemoLock(name, STATE_LOCKED, False, host, password, force_udp, unlock_timeout),
        ]
    )


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Demo config entry."""
    await async_setup_platform(hass, {}, async_add_entities)


class DemoLock(LockDevice):
    """Representation of a Demo lock."""

    def __init__(self, name, state, openable=False, host="192.168.0.202", password="12345", force_udp="True", unlock_timeout=15):
        """Initialize the lock."""
        self._name = name
        self._state = state
        self._openable = openable
        self._host = host
        self._password = password
        self._force_udp = force_udp
        self._unlock_timeout = unlock_timeout
    @property
    def should_poll(self):
        """No polling needed for a demo lock."""
        return False

    @property
    def name(self):
        """Return the name of the lock if any."""
        return self._name

    @property
    def is_locked(self):
        """Return true if lock is locked."""
        return self._state == STATE_LOCKED

    def lock(self, **kwargs):
        """Lock the device."""
        self._state = STATE_LOCKED
        self.schedule_update_ha_state()

    def unlock(self, **kwargs):
        """Unlock the device."""
        conn = None
        zk = ZK(self._host, password=self._password, force_udp=self._force_udp)
        try:
            conn = zk.connect()
            conn.unlock(self._unlock_timeout)
        finally:
            if conn:
                conn.enable_device()
                conn.disconnect()
        self._state = STATE_UNLOCKED
        self.schedule_update_ha_state()
        time.sleep(self._unlock_timeout)
        self.lock()

    def open(self, **kwargs):
        """Open the door latch."""
        self._state = STATE_UNLOCKED
        self.schedule_update_ha_state()

    @property
    def supported_features(self):
        """Flag supported features."""
        if self._openable:
            return SUPPORT_OPEN
