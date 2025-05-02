import logging


def get_logger(name: str):
    """
    Inspired by: https://docs.python.org/3/howto/logging.html#configuring-logging
    """

    log_level = logging.DEBUG
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(log_level)

    # create formatter
    formatter = logging.Formatter(
        fmt="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # add formatter to ch
    ch.setFormatter(formatter)

    # remove existing handlers
    logger.handlers = []

    # add ch to logger
    logger.addHandler(ch)

    return logger
