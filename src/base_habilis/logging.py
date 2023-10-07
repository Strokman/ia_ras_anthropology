# # from logging.config import dictConfig

# log_format = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

# logger_conf = {
#     'version': 1,
#     'formatters': {'default': {
#         'format': log_format,
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }, },
#     'root': {
#         'level': 'INFO',
#         'handlers': ['wsgi']
#     }
# }


log_format = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

log_conf = {
    'version': 1,
    'formatters': {'default': {
        'format': log_format, 'datefmt': '%Y-%m-%d %H:%M:%S',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }, },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}
