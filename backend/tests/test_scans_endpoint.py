import time
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app
from src.database.domain_task_data import Domain_Task_Data
from src.database.redis import Redis_Controller, RECORDED_DOMAIN_TASK_LIST, RECORDED_DOMAIN_TASK_BY_DOMAIN, RECORDED_DOMAIN_TASK_BY_UUID

client = TestClient(app)


def make_finished_task(domain: str) -> Domain_Task_Data:
    task = Domain_Task_Data.create(domain)
    task.end_time = int(time.time())
    return task


class TestScansEndpoint:
    """Tests for the /api/scans endpoint"""

    def teardown_method(self):
        rc = Redis_Controller()
        for key in rc._redis.scan_iter(f"{RECORDED_DOMAIN_TASK_BY_UUID}:*"):
            rc._redis.delete(key)
        for key in rc._redis.scan_iter(f"{RECORDED_DOMAIN_TASK_BY_DOMAIN}:*"):
            rc._redis.delete(key)
        rc._redis.delete(RECORDED_DOMAIN_TASK_LIST)

    def test_scans_recent_scans(self):
        """cehck correct fields, duration, and ordering"""
        older = make_finished_task("older-scan.example")
        older.end_time = older.start_time + 42
        Redis_Controller().record_domain_task(older)

        newer = make_finished_task("newer-scan.example")
        newer.end_time = int(time.time())
        Redis_Controller().record_domain_task(newer)

        response = client.get("/api/scans")
        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
        assert data[0]["task_id"] == str(newer.uuid)
        assert data[1]["task_id"] == str(older.uuid)
        assert data[1]["domain"] == older.domain
        assert "start_time" in data[1]
        assert "end_time" in data[1]
        assert data[1]["duration"] == 42

    def test_scans_limit_parameter(self):
        """limit parameter caps the number of results"""
        for i in range(5):
            Redis_Controller().record_domain_task(make_finished_task(f"limit-test-{i}.example"))

        response = client.get("/api/scans?limit=2")
        assert response.status_code == 200
        assert len(response.json()) <= 2
