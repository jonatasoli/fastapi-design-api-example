import logging
import sys
from loguru import logger
from config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())
        except Exception as e:
            raise e


def init_log():
    try:
        logger.remove()
        logging.getLogger().handlers = [InterceptHandler()]

        _time = "<fg #ffb86c>{time:DD-MM-YYYY HH:mm:ss}</fg #ffb86c>"
        _level = "<m>{level}</m>"
        _message = "<level>{message}</level>"
        logger.add(
            sys.stdout,
            colorize=True,
            level=settings.LOG_LEVEL,
            format=f"{_time} {_level} {_message}",
            backtrace=settings.LOG_BACKTRACE,
            diagnose=settings.DIAGNOSE,
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        # logger.debug("finish init log")
        for _log in [
            "uvicorn",
            "uvicorn.error",
            "fastapi",
            "gunicorn",
            "gunicorn.access",
            "gunicorn.error",
        ]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
    except Exception as e:
        raise e


def report_log_error(
    error_code,
    context_globals,
    error_exception,
    owner="",
    **kwargs,
):
    _user = f"USER: {owner}"
    _main_session = kwargs.get("main-session")
    _session = kwargs.get("session")
    _error_owner = f"{_user} | {_main_session} | {_session}"
    error_logger = [
        _error_owner,
        error_code.name,
        error_code.value,
        context_globals["__name__"],
        str(error_exception),
    ]
    ",".join(error_logger)
    logger.error(error_logger)
    logger.exception(error_exception)


def report_log_trace():
    ...
