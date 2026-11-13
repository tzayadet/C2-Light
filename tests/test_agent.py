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

    def test_rejects_embedded_credentials_and_non_base_paths(self):
        for url in (
            "http://user:pass@127.0.0.1:8000",
            "http://127.0.0.1:8000/proxy",
            "http://127.0.0.1:8000/?next=example.com",
            "http://127.0.0.1:8000/#fragment",
        ):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_server_url(url)

    def test_rejects_malformed_ports_and_control_characters(self):
        for url in (
            "http://127.0.0.1:99999",
            "http://127.0.0.1:8000\\n",
        ):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    validate_server_url(url)


if __name__ == "__main__":
    unittest.main()
