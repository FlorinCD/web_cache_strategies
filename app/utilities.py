import time

# Simulated network data (always current)
NETWORK_DATA = {f"user:{i}": f"User {i} - Updated" for i in range(1, 1001)}

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


