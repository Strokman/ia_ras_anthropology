# from logging.config import dictConfig

# log_format = '%(asctime)s - %(levelname)s in %(module)s: %(message)s'

# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': log_format, 'datefmt': '%Y-%m-%d %H:%M:%S',
#     }},
#     'handlers': {'wsgi': {
#         'level': 'INFO',
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://sys.stderror',
#         'formatter': 'default'
#     }, },
#     'root': {
#         'level': 'WARNING',
#         'handlers': ['wsgi']
#     }
# })
