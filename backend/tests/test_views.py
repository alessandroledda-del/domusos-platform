import pytest
from rest_framework import status
from backend.models import User, Company, Property


@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users_authenticated(self, auth_client, admin_user):
        response = auth_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_users_unauthenticated(self, api_client):
        response = api_client.get('/api/users/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_user(self, auth_client):
        data = {
            'email': 'newuser@test.com',
            'password': 'newpass123!',
            'nome': 'New',
            'cognome': 'User',
            'ruolo': 'user',
            'stato': 'active',
        }
        response = auth_client.post('/api/users/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'newuser@test.com'
        assert 'password' not in response.data

    def test_retrieve_user(self, auth_client, admin_user):
        response = auth_client.get(f'/api/users/{admin_user.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == admin_user.email

    def test_update_user(self, auth_client, admin_user):
        data = {
            'email': admin_user.email,
            'nome': 'Updated',
            'cognome': admin_user.cognome,
            'ruolo': admin_user.ruolo,
            'stato': admin_user.stato,
        }
        response = auth_client.put(f'/api/users/{admin_user.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome'] == 'Updated'

    def test_partial_update_user(self, auth_client, admin_user):
        response = auth_client.patch(
            f'/api/users/{admin_user.id}/', {'nome': 'Patched'}, format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['nome'] == 'Patched'

    def test_delete_user(self, auth_client, db):
        user = User.objects.create_user(
            email='todelete@test.com',
            password='delete123!',
            nome='Delete',
            cognome='Me',
        )
        response = auth_client.delete(f'/api/users/{user.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(id=user.id).exists()

    def test_me_endpoint(self, auth_client, admin_user):
        response = auth_client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == admin_user.email

    def test_set_password(self, auth_client, admin_user):
        response = auth_client.post(
            f'/api/users/{admin_user.id}/set_password/',
            {'password': 'newpassword123!'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        admin_user.refresh_from_db()
        assert admin_user.check_password('newpassword123!')

    def test_set_password_missing_field(self, auth_client, admin_user):
        response = auth_client.post(
            f'/api/users/{admin_user.id}/set_password/',
            {},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_read_only_user_cannot_create(self, user_client):
        data = {
            'email': 'blocked@test.com',
            'password': 'blocked123!',
            'nome': 'Blocked',
            'cognome': 'User',
            'ruolo': 'user',
            'stato': 'active',
        }
        response = user_client.post('/api/users/', data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestCompanyViewSet:
    def test_list_companies(self, auth_client, company):
        response = auth_client.get('/api/companies/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_create_company(self, auth_client):
        data = {
            'ragione_sociale': 'New Company S.p.A.',
            'partita_iva': '98765432109',
            'tipo_cliente': 'pme',
            'email': 'newcompany@test.com',
        }
        response = auth_client.post('/api/companies/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['ragione_sociale'] == 'New Company S.p.A.'

    def test_retrieve_company(self, auth_client, company):
        response = auth_client.get(f'/api/companies/{company.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['ragione_sociale'] == company.ragione_sociale

    def test_update_company(self, auth_client, company):
        data = {
            'ragione_sociale': company.ragione_sociale,
            'partita_iva': company.partita_iva,
            'tipo_cliente': 'pme',
            'email': company.email,
        }
        response = auth_client.put(f'/api/companies/{company.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['tipo_cliente'] == 'pme'

    def test_delete_company(self, auth_client, company):
        company_id = company.id
        response = auth_client.delete(f'/api/companies/{company.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Company.objects.filter(id=company_id).exists()

    def test_company_properties_action(self, auth_client, company, property_obj):
        response = auth_client.get(f'/api/companies/{company.id}/properties/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_company_unauthenticated(self, api_client):
        response = api_client.get('/api/companies/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestPropertyViewSet:
    def test_list_properties(self, auth_client, property_obj):
        response = auth_client.get('/api/properties/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_create_property(self, auth_client, company):
        data = {
            'company': company.id,
            'indirizzo': 'Via Garibaldi 5',
            'comune': 'Torino',
            'provincia': 'TO',
            'foglio': '002',
            'particella': '456',
            'categoria_catastale': 'B/4',
            'status': 'active',
        }
        response = auth_client.post('/api/properties/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['comune'] == 'Torino'

    def test_retrieve_property(self, auth_client, property_obj):
        response = auth_client.get(f'/api/properties/{property_obj.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['indirizzo'] == property_obj.indirizzo

    def test_filter_by_company(self, auth_client, property_obj, company):
        response = auth_client.get(f'/api/properties/?company_id={company.id}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_update_score(self, auth_client, property_obj):
        response = auth_client.post(
            f'/api/properties/{property_obj.id}/update_score/',
            {'domus_score': 88.5},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        property_obj.refresh_from_db()
        assert float(property_obj.domus_score) == 88.5

    def test_update_status(self, auth_client, property_obj):
        response = auth_client.post(
            f'/api/properties/{property_obj.id}/update_status/',
            {'status': 'archived'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        property_obj.refresh_from_db()
        assert property_obj.status == 'archived'

    def test_update_status_invalid(self, auth_client, property_obj):
        response = auth_client.post(
            f'/api/properties/{property_obj.id}/update_status/',
            {'status': 'invalid_status'},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_by_company_action(self, auth_client, company, property_obj):
        response = auth_client.get(f'/api/properties/by_company/?company_id={company.id}')
        assert response.status_code == status.HTTP_200_OK

    def test_by_company_missing_param(self, auth_client):
        response = auth_client.get('/api/properties/by_company/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_property_unauthenticated(self, api_client):
        response = api_client.get('/api/properties/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestJWTAuthentication:
    def test_obtain_token(self, api_client, admin_user):
        response = api_client.post(
            '/api/token/',
            {'email': 'admin@test.com', 'password': 'admin123!'},
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_obtain_token_invalid_credentials(self, api_client):
        response = api_client.post(
            '/api/token/',
            {'email': 'wrong@test.com', 'password': 'wrongpass'},
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token(self, api_client, admin_user):
        response = api_client.post(
            '/api/token/',
            {'email': 'admin@test.com', 'password': 'admin123!'},
            format='json',
        )
        refresh_token = response.data['refresh']
        refresh_response = api_client.post(
            '/api/token/refresh/',
            {'refresh': refresh_token},
            format='json',
        )
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data


@pytest.mark.django_db
class TestHealthEndpoints:
    def test_health_endpoint(self, api_client):
        response = api_client.get('/health/')
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['status'] == 'ok'

    def test_readiness_endpoint(self, api_client):
        response = api_client.get('/health/ready/')
        assert response.status_code in (
            status.HTTP_200_OK,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
        data = response.json()
        assert 'status' in data
        # Accept both flat and nested database status formats
        assert 'database' in data or ('checks' in data and 'database' in data.get('checks', {}))
