# from logging.config import dictConfig
# import os

# log_format = '%(asctime)s - %(levelname)s in %(module)s: %(message)s'
# pth = os.getcwd() + '/logs/flask.log'

# print(pth)
# dictConfig({
#     'version': 1,
#     'formatters': {'default': {
#         'format': log_format,
#     }},
#     'handlers': {'wsgi': {
#         'class': 'logging.StreamHandler',
#         'stream': 'ext://flask.logging.wsgi_errors_stream',
#         'formatter': 'default'
#     }, "file": {
#                 "class": "logging.handlers.TimedRotatingFileHandler",
#                 "filename": "flask.log",
#                 "when": "D",
#                 "interval": 10,
#                 "backupCount": 5,
#                 "formatter": "default",
#             }, },
#     'root': {
#         'level': 'WARNING',
#         'handlers': ['wsgi', 'file']
#     }
# })
