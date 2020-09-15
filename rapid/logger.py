from loguru import logger
import logging
import sys
import datetime
from sanic import log

log_path = "./logs"
date = datetime.date.today()


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        msg = self.format(record)
        logger_opt.log(record.levelno, msg)


logging.basicConfig(handlers=[InterceptHandler()], level=0)
logger.configure(handlers=[{"sink": sys.stderr, "level": 'INFO'}])  # 配置日志到标准输出流
logger.add(
    f"{log_path}/{date}.log", rotation="100 MB", encoding='utf-8', colorize=False, level='INFO'
)  # 配置日志到输出到文件
