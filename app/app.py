from flask import Flask, current_app
from flask_caching import Cache


def create_app():
    app = Flask(__name__)

    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = 'localhost'
    app.config['CACHE_REDIS_PORT'] = 6379
    app.config['CACHE_DEFAULT_TIMEOUT'] = 50  # TTL

    cache_obj = Cache(app)

    from .views import routes
    app.register_blueprint(routes)

    app.cache = cache_obj

    return app
