import django_filters

from .models import Company, Property, User


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    nome = django_filters.CharFilter(lookup_expr='icontains')
    cognome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['ruolo', 'stato', 'email', 'nome', 'cognome']


class CompanyFilter(django_filters.FilterSet):
    ragione_sociale = django_filters.CharFilter(lookup_expr='icontains')
    partita_iva = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Company
        fields = ['tipo_cliente', 'ragione_sociale', 'partita_iva']


class PropertyFilter(django_filters.FilterSet):
    comune = django_filters.CharFilter(lookup_expr='icontains')
    provincia = django_filters.CharFilter(lookup_expr='iexact')
    company_id = django_filters.NumberFilter(field_name='company_id')
    min_domus_score = django_filters.NumberFilter(field_name='domus_score', lookup_expr='gte')
    max_domus_score = django_filters.NumberFilter(field_name='domus_score', lookup_expr='lte')

    class Meta:
        model = Property
        fields = ['company_id', 'status', 'comune', 'provincia', 'min_domus_score', 'max_domus_score']
