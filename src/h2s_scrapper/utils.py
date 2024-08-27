import logging


def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """
    Set up a logger with the specified name and logging level.

    :param name: The name of the logger.
    :param level: The logging level (default is logging.DEBUG).
    :return: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Check if the logger already has handlers attached to avoid adding multiple handlers
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level)
    return logger
