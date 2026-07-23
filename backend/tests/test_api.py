from unittest.mock import patch

from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from backend.models import User


class APITestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_user(
            email='admin@test.com',
            password='admin12345!',
            nome='Admin',
            cognome='User',
            ruolo='admin',
            stato='active',
            is_staff=True,
            is_superuser=True,
        )
        cls.manager_user = User.objects.create_user(
            email='manager@test.com',
            password='manager12345!',
            nome='Manager',
            cognome='User',
            ruolo='manager',
            stato='active',
        )
        cls.regular_user = User.objects.create_user(
            email='user@test.com',
            password='user12345!',
            nome='Regular',
            cognome='User',
            ruolo='user',
            stato='active',
        )
        cls.other_user = User.objects.create_user(
            email='other@test.com',
            password='other12345!',
            nome='Other',
            cognome='User',
            ruolo='user',
            stato='active',
        )

    def authenticate(self, user):
        self.client.force_authenticate(user=user)


class PasswordChangeAuthorizationTests(APITestBase):
    def test_manager_cannot_change_admin_password(self):
        self.authenticate(self.manager_user)

        response = self.client.post(
            f'/api/users/{self.admin_user.id}/set_password/',
            {'password': 'new-admin-password!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['code'], 'permission_denied')
        self.assertIn('X-Trace-Id', response.headers)

    def test_regular_user_cannot_change_another_user_password(self):
        self.authenticate(self.regular_user)

        response = self.client.post(
            f'/api/users/{self.other_user.id}/set_password/',
            {'password': 'new-user-password!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['code'], 'permission_denied')

    def test_regular_user_can_change_own_password(self):
        self.authenticate(self.regular_user)

        response = self.client.post(
            f'/api/users/{self.regular_user.id}/set_password/',
            {'password': 'updated-user-password!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password('updated-user-password!'))

    def test_admin_can_change_other_user_password(self):
        self.authenticate(self.admin_user)

        response = self.client.post(
            f'/api/users/{self.other_user.id}/set_password/',
            {'password': 'admin-reset-password!'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.other_user.refresh_from_db()
        self.assertTrue(self.other_user.check_password('admin-reset-password!'))


class APIErrorContractTests(APITestBase):
    def test_invalid_login_uses_machine_friendly_error_format(self):
        response = self.client.post(
            '/api/token/',
            {'email': self.admin_user.email, 'password': 'wrong-password'},
            format='json',
        )

        payload = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(payload['code'], 'no_active_account')
        self.assertIn('message', payload)
        self.assertIn('details', payload)
        self.assertEqual(payload['trace_id'], response.headers['X-Trace-Id'])

    def test_validation_error_includes_trace_id(self):
        self.authenticate(self.admin_user)

        response = self.client.post(
            f'/api/users/{self.other_user.id}/set_password/',
            {},
            format='json',
        )

        payload = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(payload['code'], 'validation_error')
        self.assertEqual(payload['trace_id'], response.headers['X-Trace-Id'])
        self.assertIn('password', payload['details'])


class HealthEndpointTests(APITestBase):
    def test_live_endpoint_is_ok(self):
        response = self.client.get('/health/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], 'ok')

    @override_settings(REDIS_HEALTHCHECK_URL='redis://cache:6379/0')
    @patch('backend.health.Redis.from_url')
    def test_ready_endpoint_reports_redis_degraded_when_ping_fails(self, from_url):
        from redis.exceptions import RedisError

        from_url.return_value.ping.side_effect = RedisError('redis unavailable')

        response = self.client.get('/health/ready/')

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.json()['status'], 'degraded')
        self.assertEqual(response.json()['checks']['redis'], 'error')
