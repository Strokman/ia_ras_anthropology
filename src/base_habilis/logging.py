from logging.config import dictConfig
import logging

logging.StreamHandler
log_format = '%(asctime)s - %(levelname)s in %(module)s: %(message)s'

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': log_format, 'datefmt': '%Y-%m-%d %H:%M:%S',
    }},
    'handlers': {'wsgi': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }, },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
