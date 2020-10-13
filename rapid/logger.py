from loguru import logger
import logging
import sys
import datetime

log_path = "./logs"
date = datetime.date.today()

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "rapid.logger.InterceptHandler",
            "formatter": "generic",
        },
        "error_console": {
            "class": "rapid.logger.InterceptHandler",
            "formatter": "generic",
        },
        "access_console": {
            "class": "rapid.logger.InterceptHandler",
            "formatter": "access",
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
            + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        msg = self.format(record)
        logger_opt.log(record.levelno, msg)


logging.basicConfig(handlers=[InterceptHandler()], level=0)
logger.configure(handlers=[{"sink": sys.stderr, "level": "INFO"}])  # 配置日志到标准输出流
logger.add(
    f"{log_path}/{date}.log",
    rotation="100 MB",
    encoding="utf-8",
    colorize=False,
    level="INFO",
)  # 配置日志到输出到文件
