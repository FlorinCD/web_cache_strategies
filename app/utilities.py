import time

# Simulated network data (always current)
NETWORK_DATA = {
    "user:1": "Alice - Updated",
    "user:2": "Bob - Updated"
}

# Logs for analysis
event_log = []
cache_stats = {
    "hits": 0,
    "misses": 0,
    "updates": 0
}


def fetch_from_network(key):
    time.sleep(1)  # Simulate latency
    return NETWORK_DATA.get(key, "Not Found")


