import time
import random

# Simulated network data (always current)
NETWORK_DATA = {f"user:{i}": f"User {i} - Updated" for i in range(1, 1001)}

# Logs for analysis
event_log = []
cache_first_stats = {
    "hits": 0,
    "misses": 0,
    "latency_hits": [],
    "latency_misses": [],
    "same_as_in_cache_counts": 0,
}

network_first_stats = {
    "updates": 0,
    "latency_network": [],
    "same_as_in_cache_counts": 0,
}

stale_while_revalidate_stats = {
    "hits": 0,
    "updates": 0,
    "misses": 0,
    "latency_stale": [],
    "latency_misses": [],
    "same_as_in_cache_counts": 0,
}


def fetch_from_network(key):
    time.sleep(random.random())  # Simulate latency
    return NETWORK_DATA.get(key, "Not Found")


