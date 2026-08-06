from unittest.mock import patch
from django.test import RequestFactory, SimpleTestCase
from .health import health_check

class HealthEndpointTest(SimpleTestCase):
    @patch("config.health.Redis.from_url")
    @patch("config.health.connection.cursor")
    def test_health_endpoint_contract(self, cursor_mock, redis_mock):
        cursor = cursor_mock.return_value.__enter__.return_value
        cursor.fetchone.return_value = [1]
        redis_mock.return_value.ping.return_value = True
        response = health_check(RequestFactory().get("/api/health/"))
        self.assertEqual(response.status_code, 200)
