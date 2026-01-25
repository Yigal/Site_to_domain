"""
Redis Credentials Resource Test
Tests that Redis credentials from .env have access to required Redis resources.
One test per required Redis resource.
"""

import pytest
import redis


@pytest.mark.credentials
@pytest.mark.redis
class TestRedisConnectionResource:
    """Test Redis connection resource."""

    def test_redis_connection(self, redis_credentials):
        """
        Test that Redis connection credentials are valid and connection is successful.
        REQUIRES: REDIS_URL environment variable
        """
        redis_url = redis_credentials["url"]

        try:
            r = redis.from_url(redis_url)
            response = r.ping()

            assert response is True
            print(f"\n✅ Redis Connection: Successfully connected to {redis_url}")

        except redis.ConnectionError as e:
            pytest.fail(f"❌ Redis connection failed - cannot reach server: {e}")
        except redis.AuthenticationError as e:
            pytest.fail(f"❌ Redis authentication failed - invalid credentials: {e}")
        except Exception as e:
            pytest.fail(f"❌ Redis connection failed: {e}")


@pytest.mark.credentials
@pytest.mark.redis
class TestRedisOperationsResource:
    """Test Redis operations resource."""

    def test_redis_operations(self, redis_credentials):
        """
        Test that Redis has permissions for required operations (strings, lists, hashes, sets).
        REQUIRES: REDIS_URL environment variable
        """
        redis_url = redis_credentials["url"]

        try:
            r = redis.from_url(redis_url)

            # Test string operations
            r.set("test:string", "value")
            assert r.get("test:string") is not None

            # Test list operations
            r.rpush("test:list", "item1", "item2")
            assert r.llen("test:list") == 2

            # Test hash operations
            r.hset("test:hash", mapping={"field": "value"})
            assert r.hget("test:hash", "field") is not None

            # Test set operations
            r.sadd("test:set", "member1", "member2")
            assert r.scard("test:set") == 2

            # Cleanup
            r.delete("test:string", "test:list", "test:hash", "test:set")

            print(f"\n✅ Redis Operations: All data structure operations available")

        except redis.ResponseError as e:
            pytest.fail(f"❌ Redis operation failed - permission denied: {e}")
        except Exception as e:
            pytest.fail(f"❌ Redis operations test failed: {e}")
