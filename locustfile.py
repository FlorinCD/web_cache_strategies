from locust import HttpUser, task, between
import random


class CacheUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def cache_first(self):
        key = random.choice([f"user:{i}" for i in range(1, 1001)])
        self.client.get(f"/cache-first/{key}")

    @task(1)
    def network_first(self):
        key = random.choice([f"user:{i}" for i in range(1, 1001)])
        self.client.get(f"/network-first/{key}")