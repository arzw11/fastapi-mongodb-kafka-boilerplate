import logging

from project.configs.general import (
    Environment,
    GeneralSettings,
)


class LoggingSettings(GeneralSettings):
    def config_server_logger(self) -> None:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s'),
        )
        logger.addHandler(handler)

    def config_local_logger(self) -> None:
        logging.basicConfig(
            level=logging.DEBUG,
            format=logging.Formatter('%(levelname)s %(asctime)s %(module)s %(message)s'),
        )

    def config_logger(self) -> None:
        if self.ENVIRONMENT == Environment.LOCAL:
            self.config_local_logger()
        else:
            self.config_server_logger()
        logging.getLogger('pymongo').setLevel(logging.WARNING)
        logging.getLogger('motor').setLevel(logging.WARNING)
        logging.getLogger("aiokafka").setLevel(logging.WARNING)
        logging.getLogger("kafka").setLevel(logging.WARNING)
