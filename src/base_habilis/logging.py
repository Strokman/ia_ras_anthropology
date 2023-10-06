from logging.config import dictConfig
import sys

log_format = '%(asctime)s - %(levelname)s in %(module)s: %(message)s'

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': log_format, 'datefmt': '%Y-%m-%d %H:%M:%S',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': sys.stdout,
        'formatter': 'default'
    }, },
    'root': {
        'level': 'WARNING',
        'handlers': ['wsgi']
    }
})
