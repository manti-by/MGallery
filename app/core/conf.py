import os

settings = {
    'gallery': os.path.dirname(os.path.abspath(__file__)),
    'database': 'postgresql://mgallery:pa55word@mgallery-postgres/mgallery',
    'celery_broker': 'redis://mgallery-redis:6379/0',
    'logging': {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
        }
    }
}
