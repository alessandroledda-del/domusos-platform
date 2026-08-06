from django.test import TestCase
from .models import User
from .serializers import RegisterSerializer

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username="demo",
            email="demo@example.com",
            password="strong-pass-123",
        )
        self.assertEqual(user.email, "demo@example.com")

    def test_public_registration_cannot_select_admin_role(self):
        serializer = RegisterSerializer(data={
            "username": "public-user",
            "email": "public@example.com",
            "password": "strong-pass-123",
            "first_name": "Public",
            "last_name": "User",
            "role": "ADMIN",
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.role, User.Role.CLIENT)
