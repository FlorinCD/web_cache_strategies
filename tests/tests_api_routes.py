import pytest
import json
import asyncio
import httpx
from app.app import create_app


def test_cache_test_unregistered(client_cleared_cache):
    response_json = client_cleared_cache.get('/cache_test/user1').data
    try:
        response_dict = json.loads(response_json)
        assert "cached" in response_dict
        assert response_dict["cached"] == "false"
    except Exception as e:
        assert False, f"Failed of: {e}"


def test_cache_test_registered(client_cleared_cache):
    response_json = client_cleared_cache.get('/cache_test/user1').data
    cached_response_json = client_cleared_cache.get('/cache_test/user1').data
    try:
        response_dict = json.loads(cached_response_json)
        assert "cached" in response_dict
        assert response_dict["cached"] == "true"
    except Exception as e:
        assert False, f"Failed of: {e}"


# can't make the test async since the server has to be running and not be an instance locally
def test_cache_first(client_cleared_cache):
    for i in range(5):
        response_json = client_cleared_cache.get(f'/cache-first/user{i}').data
        response_dict = json.loads(response_json)

        assert "source" in response_dict
        assert response_dict["source"] == "network"

        response_json = client_cleared_cache.get(f'/cache-first/user{i}').data
        response_dict = json.loads(response_json)
        assert "source" in response_dict
        assert response_dict["source"] == "cache"

