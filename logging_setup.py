import logging
import logging.config
from config import Config


def configure_logger(type_of_env: str):
    conf_dict = Config.LOGGING_CONFIG[type_of_env]

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console_formatter': {
                'format': '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'email_formatter': {
                'format': """
                        Message type:\t%(levelname)s\n
                        Function:\t%(funcName)s\n
                        Time:\t\t%(asctime)s\n
                        \n
                        Message:\n
                        %(message)s
                        --------------------------------------
                        """,
            },
            'file_formatter': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
        },
        'handlers': {},
        'loggers': {
            '': {
                'handlers': [],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }

    handler_definitions = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console_formatter',
            'stream': 'ext://sys.stdout',
        },
        'email_report': {
            'class': 'utils.SSLSMTPHandler',
            'formatter': 'email_formatter',
            'mailhost': Config.SERVER_SMTP,
            'fromaddr': Config.MAIL_SMTP,
            'credentials': (Config.MAIL_SMTP, Config.PASSWORD_SMTP),
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'file_formatter',
            'filename': 'app.log',
        }
    }

    for handler_name, handler_config in conf_dict.items():
        handler_def = handler_definitions.get(handler_name, {}).copy()
        if handler_def:
            handler_def.update(handler_config)
            logging_config['handlers'][handler_name] = handler_def
            logging_config['loggers']['']['handlers'].append(handler_name)

    logging.config.dictConfig(logging_config)


logger = logging.getLogger(__name__)
