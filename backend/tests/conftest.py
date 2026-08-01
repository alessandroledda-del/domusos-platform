import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email='admin@test.com',
        password='admin123!',
        nome='Admin',
        cognome='Test',
        ruolo='admin',
        stato='active',
    )


@pytest.fixture
def manager_user(db):
    return User.objects.create_user(
        email='manager@test.com',
        password='manager123!',
        nome='Manager',
        cognome='Test',
        ruolo='manager',
        stato='active',
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email='user@test.com',
        password='user12345!',
        nome='Regular',
        cognome='User',
        ruolo='user',
        stato='active',
    )


@pytest.fixture
def guest_user(db):
    return User.objects.create_user(
        email='guest@test.com',
        password='guest123!',
        nome='Guest',
        cognome='User',
        ruolo='guest',
        stato='active',
    )


@pytest.fixture
def auth_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def manager_client(api_client, manager_user):
    api_client.force_authenticate(user=manager_user)
    return api_client


@pytest.fixture
def user_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client


@pytest.fixture
def company(db):
    from backend.models import Company
    return Company.objects.create(
        ragione_sociale='Domus SRL',
        partita_iva='12345678901',
        tipo_cliente='enterprise',
        email='info@domus.test',
        telefono='1234567890',
    )


@pytest.fixture
def sample_company(db):
    from backend.models import Company
    return Company.objects.create(
        ragione_sociale='Test Company S.r.l.',
        partita_iva='99999999999',
        tipo_cliente='pme',
        email='company@test.com',
        telefono='+39 02 1234567',
    )


@pytest.fixture
def property_obj(db, company):
    from backend.models import Property
    return Property.objects.create(
        company=company,
        indirizzo='Via Roma 1',
        comune='Roma',
        provincia='RM',
        foglio='10',
        particella='20',
        subalterno='1',
        categoria_catastale='A/2',
        domus_score=87.5,
        status='active',
    )


@pytest.fixture
def sample_property(db, sample_company):
    from backend.models import Property
    return Property.objects.create(
        company=sample_company,
        indirizzo='Via Dante 5',
        comune='Milano',
        provincia='MI',
        foglio='001',
        particella='123',
        subalterno='01',
        categoria_catastale='A/2',
        domus_score=75.50,
        status='active',
    )

