# Global
import configparser
import logging
import logging.config

# Config
__CONFIG__ = configparser.ConfigParser()
__CONFIG__.read('.ini')

# Log
logging.config.fileConfig('log_configs.conf')
LOGS = logging.getLogger(__name__)
LOGS.setLevel(logging.INFO)
