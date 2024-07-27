import logging
import threading

class Logger:
    _instance = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
                cls._instance._configure_logger()
        return cls._instance

    def _configure_logger(self):
        # Configure the logger here
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(logging.INFO)

        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        self._logger.addHandler(ch)

    @property
    def logger(self):
        """Property to access the logger."""
        return self._logger
    
# Create a logger instance
logger = Logger().logger