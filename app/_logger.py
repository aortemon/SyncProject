import logging


class SyncLoggerFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    _format = "%(levelname)s:    by %(name)s at %(asctime)s in %(filename)s:%(lineno)d\n               %(message)s"

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logger = logging.getLogger("Sync")
logger.setLevel(logging.DEBUG)
logger.propagate = False

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(SyncLoggerFormatter())
logger.addHandler(ch)
