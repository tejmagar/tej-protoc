import logging

formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger('tej-protoc')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False


class Log:
    enabled: bool = True

    @staticmethod
    def debug(tag, message):
        if Log.enabled:
            logger.debug(f'{tag}: {message}')

    @staticmethod
    def info(tag, message):
        if Log.enabled:
            logger.info(f'{tag}: {message}')

    @staticmethod
    def warning(tag, message):
        if Log.enabled:
            logger.warning(f'{tag}: {message}')

    @staticmethod
    def error(tag, message):
        if Log.enabled:
            logger.error(f'{tag}: {message}')

    @staticmethod
    def critical(tag, message):
        if Log.enabled:
            logger.critical(f'{tag}: {message}')

