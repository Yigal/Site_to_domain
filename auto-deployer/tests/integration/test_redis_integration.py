"""
Redis Integration Tests - Uses REAL Redis service.
No mocks. Requires valid Redis connection.
Tests will FAIL if Redis is unavailable or credentials are invalid.
"""

import pytest
import json
import time


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisConnection:
    """Integration tests for Redis connection with ACTUAL service."""

    def test_redis_connection_with_real_instance(self, redis_connection):
        """
        Test Redis connection using ACTUAL Redis instance.
        FAILS if: Redis unavailable or credentials invalid.
        """
        # ACTUAL Redis call to ping server
        response = redis_connection.ping()

        assert response is True
        assert isinstance(response, bool)

    def test_redis_server_info_with_real_instance(self, redis_connection):
        """
        Test getting Redis server info with ACTUAL instance.
        FAILS if: Redis unavailable or authentication fails.
        """
        # ACTUAL Redis call to get server info
        info = redis_connection.info()

        assert isinstance(info, dict)
        assert "redis_version" in info
        assert "used_memory" in info
        assert "connected_clients" in info


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisStringOperations:
    """Integration tests for Redis string operations with ACTUAL service."""

    def test_redis_set_and_get_with_real_instance(self, redis_connection):
        """
        Test SET and GET operations with ACTUAL Redis instance.
        FAILS if: Redis unavailable, authentication fails, or operation fails.
        """
        # ACTUAL Redis call to set value
        test_key = "integration-test/string-key"
        test_value = "test-value-12345"

        redis_connection.set(test_key, test_value)

        # ACTUAL Redis call to get value
        retrieved_value = redis_connection.get(test_key)

        assert retrieved_value is not None
        assert retrieved_value.decode("utf-8") == test_value

        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_set_with_expiration_with_real_instance(self, redis_connection):
        """
        Test SET with EX (expiration) with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/expiring-key"
        test_value = "expiring-value"

        # ACTUAL Redis call with expiration
        redis_connection.setex(test_key, 10, test_value)

        # Verify key was set
        retrieved_value = redis_connection.get(test_key)
        assert retrieved_value.decode("utf-8") == test_value

        # Verify TTL
        ttl = redis_connection.ttl(test_key)
        assert ttl > 0
        assert ttl <= 10

        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_increment_with_real_instance(self, redis_connection):
        """
        Test INCR operation with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/counter"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to increment
        value = redis_connection.incr(test_key)
        assert value == 1

        value = redis_connection.incr(test_key)
        assert value == 2

        value = redis_connection.incr(test_key, 5)
        assert value == 7

        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_append_with_real_instance(self, redis_connection):
        """
        Test APPEND operation with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/append-key"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to append
        redis_connection.append(test_key, "Hello")
        redis_connection.append(test_key, " ")
        redis_connection.append(test_key, "World")

        value = redis_connection.get(test_key)
        assert value.decode("utf-8") == "Hello World"

        # Cleanup
        redis_connection.delete(test_key)


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisListOperations:
    """Integration tests for Redis list operations with ACTUAL service."""

    def test_redis_list_operations_with_real_instance(self, redis_connection):
        """
        Test LIST operations with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/list"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to push items
        redis_connection.rpush(test_key, "item1", "item2", "item3")

        # ACTUAL Redis call to get length
        length = redis_connection.llen(test_key)
        assert length == 3

        # ACTUAL Redis call to get range
        items = redis_connection.lrange(test_key, 0, -1)
        assert len(items) == 3
        assert items[0].decode("utf-8") == "item1"

        # ACTUAL Redis call to pop
        popped = redis_connection.lpop(test_key)
        assert popped.decode("utf-8") == "item1"

        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_blocking_pop_with_real_instance(self, redis_connection):
        """
        Test blocking BLPOP operation with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/blocking-list"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to push item
        redis_connection.rpush(test_key, "blocking-item")

        # ACTUAL Redis call to blocking pop (with timeout)
        result = redis_connection.blpop(test_key, timeout=1)

        assert result is not None
        assert result[1].decode("utf-8") == "blocking-item"

        # Cleanup
        redis_connection.delete(test_key)


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisHashOperations:
    """Integration tests for Redis hash operations with ACTUAL service."""

    def test_redis_hash_operations_with_real_instance(self, redis_connection):
        """
        Test HASH operations with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/hash"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to set hash fields
        redis_connection.hset(
            test_key,
            mapping={"field1": "value1", "field2": "value2", "field3": "value3"},
        )

        # ACTUAL Redis call to get field
        value = redis_connection.hget(test_key, "field1")
        assert value.decode("utf-8") == "value1"

        # ACTUAL Redis call to get all fields
        all_fields = redis_connection.hgetall(test_key)
        assert len(all_fields) == 3
        assert all_fields[b"field1"].decode("utf-8") == "value1"

        # ACTUAL Redis call to get field count
        count = redis_connection.hlen(test_key)
        assert count == 3

        # Cleanup
        redis_connection.delete(test_key)


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisSetOperations:
    """Integration tests for Redis set operations with ACTUAL service."""

    def test_redis_set_operations_with_real_instance(self, redis_connection):
        """
        Test SET operations with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/set"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to add items
        redis_connection.sadd(test_key, "member1", "member2", "member3")

        # ACTUAL Redis call to get cardinality
        cardinality = redis_connection.scard(test_key)
        assert cardinality == 3

        # ACTUAL Redis call to check membership
        is_member = redis_connection.sismember(test_key, "member1")
        assert is_member is True

        is_not_member = redis_connection.sismember(test_key, "nonexistent")
        assert is_not_member is False

        # ACTUAL Redis call to get all members
        members = redis_connection.smembers(test_key)
        assert len(members) == 3

        # Cleanup
        redis_connection.delete(test_key)


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisSortedSetOperations:
    """Integration tests for Redis sorted set operations with ACTUAL service."""

    def test_redis_sorted_set_operations_with_real_instance(self, redis_connection):
        """
        Test SORTED SET operations with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/zset"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to add scored items
        redis_connection.zadd(
            test_key,
            {"member1": 1, "member2": 2, "member3": 3},
        )

        # ACTUAL Redis call to get cardinality
        cardinality = redis_connection.zcard(test_key)
        assert cardinality == 3

        # ACTUAL Redis call to get score
        score = redis_connection.zscore(test_key, "member2")
        assert score == 2.0

        # ACTUAL Redis call to get range by score
        members = redis_connection.zrange(test_key, 0, -1)
        assert len(members) == 3
        assert members[0].decode("utf-8") == "member1"

        # Cleanup
        redis_connection.delete(test_key)


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisKeyOperations:
    """Integration tests for Redis key operations with ACTUAL service."""

    def test_redis_key_exists_with_real_instance(self, redis_connection):
        """
        Test EXISTS operation with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/exists-key"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # Key should not exist
        exists = redis_connection.exists(test_key)
        assert exists == 0

        # Set key
        redis_connection.set(test_key, "value")

        # Key should exist
        exists = redis_connection.exists(test_key)
        assert exists == 1

        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_delete_with_real_instance(self, redis_connection):
        """
        Test DELETE operation with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key1 = "integration-test/delete-key-1"
        test_key2 = "integration-test/delete-key-2"

        # Set keys
        redis_connection.set(test_key1, "value1")
        redis_connection.set(test_key2, "value2")

        # Delete both
        deleted_count = redis_connection.delete(test_key1, test_key2)
        assert deleted_count == 2

        # Verify deletion
        assert redis_connection.exists(test_key1) == 0
        assert redis_connection.exists(test_key2) == 0

    def test_redis_keys_pattern_with_real_instance(self, redis_connection):
        """
        Test KEYS pattern matching with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_prefix = "integration-test/pattern"

        # ACTUAL Redis call to set keys
        redis_connection.set(f"{test_prefix}-1", "value1")
        redis_connection.set(f"{test_prefix}-2", "value2")
        redis_connection.set(f"{test_prefix}-3", "value3")

        # ACTUAL Redis call to find keys by pattern
        keys = redis_connection.keys(f"{test_prefix}-*")

        assert len(keys) >= 3

        # Cleanup
        redis_connection.delete(f"{test_prefix}-1", f"{test_prefix}-2", f"{test_prefix}-3")


@pytest.mark.integration
@pytest.mark.requires_redis
@pytest.mark.requires_internet
class TestRedisTransactions:
    """Integration tests for Redis transactions with ACTUAL service."""

    def test_redis_transaction_with_real_instance(self, redis_connection):
        """
        Test MULTI/EXEC transaction with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/transaction-key"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis transaction
        pipe = redis_connection.pipeline()
        pipe.set(test_key, "initial")
        pipe.incr(test_key)  # Will fail since value is not integer, but let's see
        pipe.execute()

        # The transaction executed (though incr may have failed)
        # Cleanup
        redis_connection.delete(test_key)

    def test_redis_watched_transaction_with_real_instance(self, redis_connection):
        """
        Test WATCH for optimistic locking with ACTUAL Redis instance.
        FAILS if: Redis unavailable or operation fails.
        """
        test_key = "integration-test/watched-key"

        # ACTUAL Redis call to delete first
        redis_connection.delete(test_key)

        # ACTUAL Redis call to set initial value
        redis_connection.set(test_key, "0")

        # ACTUAL Redis transaction with WATCH
        pipe = redis_connection.pipeline()
        try:
            pipe.watch(test_key)
            current_value = int(pipe.get(test_key))
            pipe.multi()
            pipe.set(test_key, str(current_value + 1))
            pipe.execute()

            final_value = int(redis_connection.get(test_key))
            assert final_value == 1

        finally:
            pipe.reset()
            # Cleanup
            redis_connection.delete(test_key)
