import unittest

from agent import run_task, validate_server_url


class AgentSafetyTests(unittest.TestCase):
    def test_only_fixed_status_task_is_supported(self):
        self.assertIn("no host commands executed", run_task("report_status"))

    def test_unknown_task_is_rejected(self):
        with self.assertRaises(ValueError):
            run_task("whoami")

    def test_loopback_server_is_allowed(self):
        self.assertEqual(validate_server_url("http://127.0.0.1:8000"), "http://127.0.0.1:8000")

    def test_non_loopback_server_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_server_url("http://example.com:8000")

    def test_https_is_not_silently_accepted(self):
        with self.assertRaises(ValueError):
            validate_server_url("https://127.0.0.1:8000")


if __name__ == "__main__":
    unittest.main()
