import logging
import signal

logger = logging.getLogger(__name__)


class SigHandler:
    """SuperClass of signal handling, do not use directly
    """

    def __init__(self):
        self.callbacks = []

    def add_callback(self, callback, **kwargs):
        """Add the couple callback, args to the list of
        callback to call when signal is received.
        """
        self.callbacks.append({"what": callback, "with": kwargs})

    def _sighandler(self, sign, frame):
        logger.debug("Received signal < %s / %s >", sign, frame)
        for registered in self.callbacks:
            registered["what"](**registered["with"])


class SigTermHandler(SigHandler):
    """SIGTERM Handler. Listen to signal.SIGTERM (15)
    """

    def __init__(self):
        super(SigTermHandler, self).__init__()
        signal.signal(signal.SIGTERM, self._sighandler)
