import time
import threading
from flask import jsonify, Blueprint, current_app
from app.utilities import fetch_from_network, event_log, cache_first_stats, network_first_stats, stale_while_revalidate_stats


routes = Blueprint('routes', __name__)


@routes.route('/cache_test/<key>', methods=['GET', 'POST'])
def cache_test(key):
    cache_obj = current_app.cache
    cached = cache_obj.get(key)

    if cached:
        return jsonify({"cached": "true"})
    else:
        cache_obj.set(key, "true")
        return jsonify({"cached": "false"})


@routes.route('/cache-first/<key>', methods=['GET', 'POST'])
def cache_first(key):
    cache_obj = current_app.cache
    start_time = time.time()  # Start timer
    cached = cache_obj.get(key)
    if cached:
        cache_first_stats["hits"] += 1
        event_log.append({"event": "cache_hit", "key": key, "time": time.time()})
        latency = time.time() - start_time  # Latency for cache hit
        cache_first_stats["latency_hits"].append(latency)
        return jsonify({"source": "cache", "data": cached, "latency": latency})
    else:
        cache_first_stats["misses"] += 1
        event_log.append({"event": "cache_miss", "key": key, "time": time.time()})
        data = fetch_from_network(key)
        cache_obj.set(key, data)
        latency = time.time() - start_time  # Latency for network fetch
        cache_first_stats["latency_misses"].append(latency)
        return jsonify({"source": "network", "data": data, "latency": latency})


@routes.route('/network-first/<key>', methods=['GET', 'POST'])
def network_first(key):
    cache_obj = current_app.cache
    start_time = time.time()  # Start timer
    data = fetch_from_network(key)
    cache_obj.set(key, data)
    network_first_stats["updates"] += 1
    event_log.append({"event": "network_fetch", "key": key, "time": time.time()})
    latency = time.time() - start_time  # Latency for network fetch
    network_first_stats["latency_network"].append(latency)
    return jsonify({"source": "network", "data": data, "latency": latency})


@routes.route('/stale-while-revalidate/<key>', methods=['GET', 'POST'])
def stale_while_revalidate(key):
    cache_obj = current_app.cache
    start_time = time.time()  # Start timer
    cached = cache_obj.get(key)

    if cached:
        def background_refresh():
            fresh = fetch_from_network(key)
            cache_obj.set(key, fresh)
            stale_while_revalidate_stats["updates"] += 1
            event_log.append({"event": "background_refresh", "key": key, "time": time.time()})

        threading.Thread(target=background_refresh).start()
        stale_while_revalidate_stats["hits"] += 1
        event_log.append({"event": "cache_stale", "key": key, "time": time.time()})
        latency = time.time() - start_time  # Latency for stale cache hit
        stale_while_revalidate_stats["latency_stale"].append(latency)
        return jsonify({"source": "cache (stale)", "data": cached, "latency": latency})
    else:
        data = fetch_from_network(key)
        cache_obj.set(key, data)
        stale_while_revalidate_stats["misses"] += 1
        event_log.append({"event": "cache_miss", "key": key, "time": time.time()})
        latency = time.time() - start_time  # Latency for network fetch
        stale_while_revalidate_stats["latency_misses"].append(latency)
        return jsonify({"source": "network", "data": data, "latency": latency})


@routes.route('/cache_first_stats', methods=['GET', 'POST'])
def strategy_cache_first_stats():
    return jsonify(cache_first_stats)


@routes.route('/network_first_stats', methods=['GET', 'POST'])
def strategy_network_first_stats():
    return jsonify(network_first_stats)


@routes.route('/stale_while_revalidate_stats', methods=['GET', 'POST'])
def strategy_stale_while_revalidate_stats():
    return jsonify(stale_while_revalidate_stats)


@routes.route('/log', methods=['GET', 'POST'])
def log():
    count_hits, count_misses = 0, 0
    for event in event_log:
        if "event" in event and event["event"] == "cache_hit":
            count_hits += 1
        elif "event" in event and event["event"] == "cache_miss":
            count_misses += 1
    return jsonify(["count_hits", count_hits] + ["count_misses", count_misses] + event_log[-50:])  # Last 50 events


@routes.route('/clear-cache', methods=['GET', 'POST'])
def clear_cache():
    global cache_first_stats, network_first_stats, stale_while_revalidate_stats
    cache_obj = current_app.cache
    cache_obj.clear()

    cache_first_stats = {"hits": 0, "misses": 0, "latency_hits": [], "latency_misses": []}
    network_first_stats = {"updates": 0, "latency_network": []}
    stale_while_revalidate_stats = {"hits": 0, "updates": 0, "misses": 0, "latency_stale": 0, "latency_misses": 0}

    event_log.clear()
    return jsonify({"status": "Cache cleared"})

