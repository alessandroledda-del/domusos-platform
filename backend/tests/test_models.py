import pytest
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from backend.models import Company, Property

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123!',
            nome='Test',
            cognome='User',
        )
        assert user.email == 'test@example.com'
        assert user.nome == 'Test'
        assert user.cognome == 'User'
        assert user.ruolo == 'user'
        assert user.stato == 'active'
        assert user.check_password('testpass123!')

    def test_create_user_without_email_raises(self):
        with pytest.raises(ValueError, match='The Email field must be set'):
            User.objects.create_user(email='', password='pass123!')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='super@example.com',
            password='superpass123!',
            nome='Super',
            cognome='Admin',
        )
        assert superuser.is_staff is True
        assert superuser.is_superuser is True
        assert superuser.ruolo == 'admin'

    def test_user_str_representation(self):
        user = User.objects.create_user(
            email='john@example.com',
            password='pass123!',
            nome='John',
            cognome='Doe',
        )
        assert str(user) == 'John Doe (john@example.com)'

    def test_user_username_field_is_email(self):
        assert User.USERNAME_FIELD == 'email'

    def test_manager_role_in_choices(self):
        roles = [choice[0] for choice in User.ROLE_CHOICES]
        assert 'manager' in roles
        assert 'admin' in roles
        assert 'user' in roles
        assert 'guest' in roles

    def test_user_ordering_is_by_created_at_desc(self):
        user1 = User.objects.create_user(
            email='a@example.com', password='pass1!', nome='A', cognome='B'
        )
        user2 = User.objects.create_user(
            email='b@example.com', password='pass2!', nome='C', cognome='D'
        )
        users = list(User.objects.all())
        assert users[0] == user2
        assert users[1] == user1

    def test_create_user_with_manager_role(self):
        user = User.objects.create_user(
            email='manager@example.com',
            password='securePass123!',
            nome='Mario',
            cognome='Rossi',
            ruolo='manager',
        )
        assert user.check_password('securePass123!')
        assert user.ruolo == 'manager'
        assert ('manager', 'Manager') in User.ROLE_CHOICES


@pytest.mark.django_db
class TestCompanyModel:
    def test_create_company(self, company):
        assert company.ragione_sociale == 'Domus SRL'
        assert company.partita_iva == '12345678901'
        assert company.tipo_cliente == 'enterprise'

    def test_company_str_representation(self, company):
        assert str(company) == 'Domus SRL (12345678901)'

    def test_company_and_property_str_representation(self):
        co = Company.objects.create(
            ragione_sociale='Acme SPA',
            partita_iva='11111111111',
            tipo_cliente='pme',
            email='acme@example.com',
        )
        prop = Property.objects.create(
            company=co,
            indirizzo='Via Milano 10',
            comune='Milano',
            provincia='MI',
            foglio='22',
            particella='18',
            categoria_catastale='A/3',
            status='active',
        )
        assert str(co) == 'Acme SPA (11111111111)'
        assert str(prop) == 'Via Milano 10, Milano (MI)'

    def test_company_unique_partita_iva(self, company):
        with pytest.raises(IntegrityError):
            Company.objects.create(
                ragione_sociale='Another Company',
                partita_iva='12345678901',
                tipo_cliente='pme',
                email='another@test.com',
            )

    def test_company_unique_ragione_sociale(self, company):
        with pytest.raises(IntegrityError):
            Company.objects.create(
                ragione_sociale='Domus SRL',
                partita_iva='55555555555',
                tipo_cliente='pme',
                email='another@test.com',
            )


@pytest.mark.django_db
class TestPropertyModel:
    def test_create_property(self, property_obj, company):
        assert property_obj.indirizzo == 'Via Roma 1'
        assert property_obj.comune == 'Roma'
        assert property_obj.provincia == 'RM'
        assert property_obj.company == company
        assert float(property_obj.domus_score) == 87.5
        assert property_obj.status == 'active'

    def test_property_str_representation(self, property_obj):
        assert str(property_obj) == 'Via Roma 1, Roma (RM)'

    def test_property_company_cascade_delete(self, company, property_obj):
        assert Property.objects.count() == 1
        company.delete()
        assert Property.objects.count() == 0

    def test_property_status_choices(self):
        valid_statuses = [choice[0] for choice in Property.STATUS_CHOICES]
        assert 'active' in valid_statuses
        assert 'inactive' in valid_statuses
        assert 'archived' in valid_statuses

    def test_property_related_name(self, company, property_obj):
        assert company.properties.count() == 1
        assert company.properties.first() == property_obj
