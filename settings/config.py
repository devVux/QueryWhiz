from logging.config import dictConfig


class Common(object):
    swaggerTemplate = {
        "swagger": "2.0",
        "info": {
            "title": "Flask QueryWhiz API",
            "description": "This API was developed using Python Flask, which provides an interface for producing and consuming messages via HTTP endpoints.",
            "version": "1.0"
        }
    }

    def __init__(self):
        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                  'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'wsgi': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://flask.logging.wsgi_errors_stream',
                    'formatter': 'default'
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['wsgi']
            }
        })

class Local(Common):
    DEBUG = True

class Production(Common):
    DEBUG = False
