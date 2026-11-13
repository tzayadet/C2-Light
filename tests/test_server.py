import unittest

from fastapi import HTTPException, status
from pydantic import ValidationError

import server


class ServerSafetyTests(unittest.TestCase):
    def setUp(self):
        server.agents.clear()

    def test_loopback_peer_validation(self):
        for address in ("127.0.0.1", "::1", "::ffff:127.0.0.1"):
            with self.subTest(address=address):
                self.assertTrue(server.is_loopback_client(address))
        for address in ("192.0.2.10", "2001:db8::1", None, "not-an-ip"):
            with self.subTest(address=address):
                self.assertFalse(server.is_loopback_client(address))

    def test_checkin_issues_token_and_fixed_status_task(self):
        registration = server.checkin(server.CheckIn(id="test-agent"))
        self.assertTrue(registration["token"])
        tasks = server.get_tasks("test-agent", registration["token"])
        self.assertEqual(tasks, ["report_status"])

    def test_invalid_agent_token_is_rejected(self):
        server.checkin(server.CheckIn(id="test-agent"))
        with self.assertRaises(HTTPException) as error:
            server.get_tasks("test-agent", "invalid-token")
        self.assertEqual(error.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unknown_task_type_is_rejected_by_schema(self):
        with self.assertRaises(ValidationError):
            server.Task(task="execute_shell")

    def test_duplicate_agent_identifier_is_rejected(self):
        server.checkin(server.CheckIn(id="test-agent"))
        with self.assertRaises(HTTPException) as error:
            server.checkin(server.CheckIn(id="test-agent"))
        self.assertEqual(error.exception.status_code, status.HTTP_409_CONFLICT)

    def test_invalid_agent_identifier_is_rejected(self):
        with self.assertRaises(HTTPException) as error:
            server.checkin(server.CheckIn(id="../outside"))
        self.assertEqual(error.exception.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_queue_has_a_fixed_capacity(self):
        registration = server.checkin(server.CheckIn(id="test-agent"))
        server.agents["test-agent"]["tasks"] = ["report_status"] * server.MAX_TASKS_PER_AGENT
        with self.assertRaises(HTTPException) as error:
            server.enqueue_status_task(
                "test-agent", server.Task(task="report_status"), registration["token"]
            )
        self.assertEqual(error.exception.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_expired_agents_are_removed(self):
        server.checkin(server.CheckIn(id="expired-agent"))
        server.agents["expired-agent"]["last_seen"] -= server.AGENT_TTL_SECONDS + 1
        with self.assertRaises(HTTPException) as error:
            server.get_tasks("expired-agent", server.agents["expired-agent"]["token"])
        self.assertEqual(error.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("expired-agent", server.agents)


if __name__ == "__main__":
    unittest.main()
