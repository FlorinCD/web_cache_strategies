import requests
import time


# Simulate requests to Flask endpoints
def simulate_requests():
    keys = ["user:1", "user:2", "user:3"]

    # Make requests in various patterns
    for i in range(10):  # Simulate 10 cycles
        for key in keys:
            print(f"Requesting {key}...")
            # Simulate a cache-first request (this will cache on first miss)
            requests.get(f"http://localhost:5000/cache-first/{key}")
            time.sleep(1)

        for key in keys:
            print(f"Requesting {key} (network-first)...")
            # Simulate a network-first request (always fetch fresh)
            requests.get(f"http://localhost:5000/network-first/{key}")
            time.sleep(1)

        for key in keys:
            print(f"Requesting {key} (stale-while-revalidate)...")
            # Simulate stale-while-revalidate request (serve stale and refresh in background)
            requests.get(f"http://localhost:5000/stale-while-revalidate/{key}")
            time.sleep(1)


if __name__ == "__main__":
    simulate_requests()
