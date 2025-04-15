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


def test_strategy_cache_first_stats(client_cleared_cache):
    try:
        response_json = client_cleared_cache.get('/cache_first_stats').data
        response = json.loads(response_json)
    except Exception as e:
        assert False, f"Failed of: {e}"
    assert "hits" in response
    assert "misses" in response
    assert "latency_hits" in response
    assert "latency_misses" in response


def test_strategy_network_first_stats(client_cleared_cache):
    try:
        response_json = client_cleared_cache.get('/network_first_stats').data
        response = json.loads(response_json)
    except Exception as e:
        assert False, f"Failed of: {e}"

    assert "updates" in response
    assert "latency_network" in response


def test_strategy_stale_while_revalidate_stats(client_cleared_cache):
    try:
        response_json = client_cleared_cache.get('/stale_while_revalidate_stats').data
        response = json.loads(response_json)
    except Exception as e:
        assert False, f"Failed of: {e}"

    assert "hits" in response
    assert "misses" in response
    assert "updates" in response
    assert "latency_stale" in response
    assert "latency_misses" in response


def test_clear_cache(client_cleared_cache, app_instance):
    try:
        response_json = client_cleared_cache.get('/cache_test/user1')
        cached_value = app_instance.cache.get("user1") or 'false'

        clear_response = client_cleared_cache.get('/clear-cache')
        cached_value = app_instance.cache.get("user1") or 'false'
        assert cached_value == 'false'
    except Exception as e:
        assert False, f"Failed of: {e}"

