import logging
import coloredlogs

logger = logging.getLogger(name="app")
logger.propagate = False  # Prevent logs from propagating to parent logger

# Configure colored logs
coloredlogs.install(
    level="DEBUG",  # Set the default logging level to DEBUG
    logger=logger,
    fmt="[%(name)s] %(asctime)s %(funcName)s %(lineno)s %(message)s",
    level_styles={
        "debug": {"color": "white"},
        "info": {"color": "cyan", "bold": True},
        "warning": {"color": "yellow", "bold": True},
        "error": {"color": "red", "bold": True},
        "critical": {"color": "white", "bold": True, "background": "red"},
    },
    field_styles={
        "name": {"color": "yellow", "bold": True},
        "asctime": {"color": "green", "bold": True},
        "funcName": {"color": "magenta", "bold": True},
        "lineno": {"color": "red", "bold": True},
    },
)
