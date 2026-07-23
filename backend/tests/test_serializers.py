import pytest
from backend.serializers import (
    UserSerializer,
    CompanySerializer,
    PropertyCreateUpdateSerializer,
    PropertySerializer,
)
from backend.models import Company, User


@pytest.mark.django_db
class TestUserSerializer:
    def test_password_is_write_only(self):
        serializer = UserSerializer()
        assert serializer.fields['password'].write_only is True

    def test_create_user_via_serializer(self):
        data = {
            'email': 'serial@test.com',
            'password': 'pass123!',
            'nome': 'Serial',
            'cognome': 'Test',
            'ruolo': 'user',
            'stato': 'active',
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.check_password('pass123!')
        assert user.email == 'serial@test.com'

    def test_update_user_password_via_serializer(self, admin_user):
        serializer = UserSerializer(admin_user, data={'password': 'newpass456!'}, partial=True)
        assert serializer.is_valid(), serializer.errors
        user = serializer.save()
        assert user.check_password('newpass456!')

    def test_invalid_email(self):
        data = {
            'email': 'not-an-email',
            'password': 'pass123!',
            'nome': 'Test',
            'cognome': 'User',
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_short_password_invalid(self):
        data = {
            'email': 'test@test.com',
            'password': 'short',
            'nome': 'Test',
            'cognome': 'User',
        }
        serializer = UserSerializer(data=data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors


@pytest.mark.django_db
class TestCompanySerializer:
    def test_serialize_company(self, company):
        serializer = CompanySerializer(company)
        data = serializer.data
        assert data['ragione_sociale'] == 'Domus SRL'
        assert data['partita_iva'] == '12345678901'

    def test_create_company_via_serializer(self):
        data = {
            'ragione_sociale': 'Serializer Company',
            'partita_iva': '11111111111',
            'tipo_cliente': 'freelance',
            'email': 'serial@company.com',
        }
        serializer = CompanySerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        company = serializer.save()
        assert company.ragione_sociale == 'Serializer Company'


@pytest.mark.django_db
class TestPropertySerializer:
    def test_serialize_property(self, property_obj):
        serializer = PropertySerializer(property_obj)
        data = serializer.data
        assert data['indirizzo'] == 'Via Roma 1'
        assert data['comune'] == 'Roma'
        assert data['provincia'] == 'RM'

    def test_create_property_via_serializer(self, company):
        data = {
            'company': company.id,
            'indirizzo': 'Via Dante 10',
            'comune': 'Torino',
            'provincia': 'TO',
            'foglio': '003',
            'particella': '789',
            'categoria_catastale': 'C/1',
            'status': 'active',
        }
        serializer = PropertyCreateUpdateSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        prop = serializer.save()
        assert prop.comune == 'Torino'
