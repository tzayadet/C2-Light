import unittest

from fastapi import HTTPException, status
from pydantic import ValidationError

import server


class ServerSafetyTests(unittest.TestCase):
    def setUp(self):
        server.agents.clear()

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


if __name__ == "__main__":
    unittest.main()
