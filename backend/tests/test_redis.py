import time
import pytest
from src.database.redis import Redis_Controller, RECORDED_DOMAIN_TASK_LIST, RECORDED_DOMAIN_TASK_BY_DOMAIN, RECORDED_DOMAIN_TASK_BY_UUID
from src.database.domain_task_data import Domain_Task_Data
from src.database.domain_name_hash_wrapper import Domain_Name_Hash_Wrapper

class TestRedisController:
    """Tests for writting and reading from Redis Controller"""

    def teardown_method(self):
        rc = Redis_Controller()
        for key in rc._redis.scan_iter(f"{RECORDED_DOMAIN_TASK_BY_UUID}:*"):
            rc._redis.delete(key)
        for key in rc._redis.scan_iter(f"{RECORDED_DOMAIN_TASK_BY_DOMAIN}:*"):
            rc._redis.delete(key)
        rc._redis.delete(RECORDED_DOMAIN_TASK_LIST)

    def test_domain_blocking(self):
        domain = "test.com"

        Redis_Controller().unblock_domain(domain) # Prevent flaky-ness
        assert Redis_Controller().block_domain(domain) is True
        assert Redis_Controller().block_domain(domain) is False

        assert Redis_Controller().is_domain_in_domain_blocklist(domain) is True
        Redis_Controller().unblock_domain(domain)
        assert Redis_Controller().is_domain_in_domain_blocklist(domain) is False

    def test_client_blocking(self):
        session_id = "1"
        domain = "test.com"

        Redis_Controller().unblock_session_id_for_domain(session_id, domain) # Prevent flaky-ness
        assert Redis_Controller().block_session_id_for_domain(session_id, domain) is True
        assert Redis_Controller().block_session_id_for_domain(session_id, domain) is False

        assert Redis_Controller().is_session_id_in_client_blocklist(session_id, domain) is True
        Redis_Controller().unblock_session_id_for_domain(session_id, domain)
        assert Redis_Controller().is_session_id_in_client_blocklist(session_id, domain) is False

    def test_recording_task_results(self):
        domainWorking = "easterEgg.com"

        data = Domain_Task_Data.create(domainWorking)

        Redis_Controller().record_domain_task(data)

        assert Redis_Controller().get_domain_task_by_uuid(data.uuid) is not None
        assert Redis_Controller().get_domain_task_by_domain_hash(Domain_Name_Hash_Wrapper().domain_hash(data.domain)) is not None

        assert Redis_Controller().get_domain_task_by_uuid("-") is None
        assert Redis_Controller().get_domain_task_by_domain_hash("-") is None

    def test_get_all_domain_tasks(self):
        """test that the tasks appear in get_all_domain_tasks"""
        task1 = Domain_Task_Data.create("all-tasks-test-1.com")
        task1.end_time = int(time.time())
        task2 = Domain_Task_Data.create("all-tasks-test-2.com")
        task2.end_time = int(time.time())
        Redis_Controller().record_domain_task(task1)
        Redis_Controller().record_domain_task(task2)

        tasks = Redis_Controller().get_all_domain_tasks()
        uuids = [str(t.uuid) for t in tasks]
        assert str(task1.uuid) in uuids
        assert str(task2.uuid) in uuids

    def test_get_all_domain_tasks_limit(self):
        """test the limit parameter caps the number of returned tasks"""
        for i in range(5):
            t = Domain_Task_Data.create(f"limit-redis-test-{i}.com")
            t.end_time = int(time.time())
            Redis_Controller().record_domain_task(t)

        tasks = Redis_Controller().get_all_domain_tasks(limit=2)
        assert len(tasks) <= 2

    def test_get_all_domain_tasks_cleans_expired(self):
        """expired UUID is removed from the task list"""
        rc = Redis_Controller()
        fake_uuid = "00000000-0000-0000-0000-000000000001"
        rc._redis.rpush(RECORDED_DOMAIN_TASK_LIST, fake_uuid)

        assert rc.get_all_domain_tasks() == []

        remaining = [u.decode() for u in rc._redis.lrange(RECORDED_DOMAIN_TASK_LIST, 0, -1)]
        assert fake_uuid not in remaining


