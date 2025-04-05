import time
import threading
from flask import jsonify, Blueprint, current_app
from app.utilities import fetch_from_network, event_log, cache_stats
import logging


routes = Blueprint('routes', __name__)


@routes.route('/cache-first/<key>', methods=['GET', 'POST'])
def cache_first(key):
    cache_obj = current_app.cache
    cached = cache_obj.get(key)
    if cached:
        cache_stats["hits"] += 1
        event_log.append({"event": "cache_hit", "key": key, "time": time.time()})
        return jsonify({"source": "cache", "data": cached})
    else:
        cache_stats["misses"] += 1
        event_log.append({"event": "cache_miss", "key": key, "time": time.time()})
        data = fetch_from_network(key)
        cache_obj.set(key, data)
        return jsonify({"source": "network", "data": data})


@routes.route('/network-first/<key>', methods=['GET', 'POST'])
def network_first(key):
    cache_obj = current_app.cache
    data = fetch_from_network(key)
    cache_obj.set(key, data)
    cache_stats["updates"] += 1
    event_log.append({"event": "network_fetch", "key": key, "time": time.time()})
    return jsonify({"source": "network", "data": data})


@routes.route('/stale-while-revalidate/<key>', methods=['GET', 'POST'])
def stale_while_revalidate(key):
    cache_obj = current_app.cache
    cached = cache_obj.get(key)
    if cached:
        def background_refresh():
            fresh = fetch_from_network(key)
            cache_obj.set(key, fresh)
            cache_stats["updates"] += 1
            event_log.append({"event": "background_refresh", "key": key, "time": time.time()})

        threading.Thread(target=background_refresh).start()
        cache_stats["hits"] += 1
        event_log.append({"event": "cache_stale", "key": key, "time": time.time()})
        return jsonify({"source": "cache (stale)", "data": cached})
    else:
        data = fetch_from_network(key)
        cache_obj.set(key, data)
        cache_stats["misses"] += 1
        event_log.append({"event": "cache_miss", "key": key, "time": time.time()})
        return jsonify({"source": "network", "data": data})


@routes.route('/stats', methods=['GET', 'POST'])
def stats():
    return jsonify(cache_stats)


@routes.route('/log', methods=['GET', 'POST'])
def log():
    return jsonify(event_log[-50:])  # Last 50 events


@routes.route('/clear-cache', methods=['GET', 'POST'])
def clear_cache():
    cache_obj = current_app.cache
    cache_obj.clear()
    cache_stats.update({"hits": 0, "misses": 0, "updates": 0})
    event_log.clear()
    return jsonify({"status": "Cache cleared"})

