from locust import HttpUser, task, between
import random
import dotenv
import os

dotenv.load_dotenv()
CACHE_STRATEGY = os.getenv("CACHING_STRATEGY")

class CacheUser(HttpUser):
    wait_time = between(1, 3)

    if CACHE_STRATEGY == "CACHE_FIRST":
        @task
        def cache_first(self):
            key = random.choice([f"user:{i}" for i in range(1, 1001)])
            self.client.get(f"/cache-first/{key}")
    elif CACHE_STRATEGY == "NETWORK_FIRST":
        @task
        def network_first(self):
            key = random.choice([f"user:{i}" for i in range(1, 1001)])
            self.client.get(f"/cache-first/{key}")
    else:
        @task
        def network_first(self):
            key = random.choice([f"user:{i}" for i in range(1, 1001)])
            self.client.get(f"/stale-while-revalidate/{key}")