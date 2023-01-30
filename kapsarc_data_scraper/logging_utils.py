import logging
import logging.config


def logger_configuration():
    # default logging configuration
    simple_formatter = {
        "format": "%(asctime)s|%(levelname)7s|%(filename)25s:%(lineno)3s %(funcName)30s()| %(message)s",
        "datefmt": "%y-%m-%d %H:%M:%S",
    }

    console_handler = {
        "class": "logging.StreamHandler",
        "level": "DEBUG",
        "formatter": "simple",
        "stream": "ext://sys.stdout",
    }

    config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"simple": simple_formatter},
        "handlers": {"console": console_handler},
        "root": {"level": "INFO", "handlers": ["console"]},
    }

    return config_dict


def get_logger(name: str = "") -> logging.Logger:
    """
    initiate a logging object
    :param name: name of the logger to use to filter logs
    :return: initiated logger object
    """
    conf = logger_configuration()
    logging.config.dictConfig(conf)
    logger = logging.getLogger(name)

    return logger
