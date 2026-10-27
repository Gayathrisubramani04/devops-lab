import unittest
import threading
import urllib.request
import urllib.error
from http.server import HTTPServer
from app import AppHandler

class AppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), AppHandler)
        cls.thread = threading.Thread(
            target=cls.server.serve_forever,
            daemon=True
        )
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_home(self):
        with urllib.request.urlopen(self.base + "/") as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"DevOps Lab", response.read())

    def test_health(self):
        with urllib.request.urlopen(self.base + "/health") as response:
            self.assertEqual(response.status, 200)
            self.assertIn(b"healthy", response.read())

    def test_metrics(self):
        with urllib.request.urlopen(self.base + "/metrics") as response:
            self.assertIn(b"devops_app_up 1", response.read())

    def test_error_endpoint(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(self.base + "/error")
        self.assertEqual(error.exception.code, 500)

if __name__ == "__main__":
    unittest.main()
