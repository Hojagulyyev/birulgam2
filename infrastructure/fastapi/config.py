# TODO: get from .env
DEBUG = True
PROJECT_NAME = "Python Clean Architecture"


APP_CONFIG = {
    "debug": DEBUG,
    "title": PROJECT_NAME,
    "version": "0.1.0-alpha.1",
    "servers": [
        {
            "url": "https://stag.example.com",
            "description": "Staging environment",
        },
        {
            "url": "https://prod.example.com",
            "description": "Production environment",
        },
    ],
    "docs_url": None,
    "redoc_url": None,
}
