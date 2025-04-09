import time

# Simulated network data (always current)
NETWORK_DATA = {f"user:{i}": f"User {i} - Updated" for i in range(1, 1001)}

# Logs for analysis
event_log = []
cache_first_stats = {
    "hits": 0,
    "misses": 0,
    "latency_hits": [],
    "latency_misses": []
}

network_first_stats = {
    "updates": 0,
    "latency_network": []
}

stale_while_revalidate_stats = {
    "hits": 0,
    "updates": 0,
    "misses": 0,
    "latency_stale": 0,
    "latency_misses": 0
}


def fetch_from_network(key):
    time.sleep(0.4)  # Simulate latency
    return NETWORK_DATA.get(key, "Not Found")


