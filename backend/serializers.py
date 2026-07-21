from rest_framework import serializers
from .models import User, Company, Property


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'nome',
            'cognome',
            'telefono',
            'ruolo',
            'stato',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Create user with hashed password"""
        user = User(**validated_data)
        user.set_password(validated_data.get('password_hash', ''))
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user, handling password hashing if provided"""
        password = validated_data.pop('password_hash', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


class UserDetailSerializer(UserSerializer):
    """Extended serializer for detailed user information"""
    
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for Company model"""
    
    class Meta:
        model = Company
        fields = [
            'id',
            'ragione_sociale',
            'partita_iva',
            'tipo_cliente',
            'email',
            'telefono',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class CompanyDetailSerializer(serializers.ModelSerializer):
    """Extended serializer for detailed company information with properties"""
    
    properties = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = [
            'id',
            'ragione_sociale',
            'partita_iva',
            'tipo_cliente',
            'email',
            'telefono',
            'created_at',
            'properties',
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_properties(self, obj):
        """Get count and list of properties for the company"""
        properties = obj.properties.all()
        return {
            'count': properties.count(),
            'items': PropertySerializer(properties, many=True).data,
        }


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model"""
    
    company_name = serializers.CharField(source='company.ragione_sociale', read_only=True)
    
    class Meta:
        model = Property
        fields = [
            'id',
            'company',
            'company_name',
            'indirizzo',
            'comune',
            'provincia',
            'foglio',
            'particella',
            'subalterno',
            'categoria_catastale',
            'domus_score',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'company_name']


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Extended serializer for detailed property information"""
    
    company = CompanySerializer(read_only=True)
    
    class Meta:
        model = Property
        fields = [
            'id',
            'company',
            'indirizzo',
            'comune',
            'provincia',
            'foglio',
            'particella',
            'subalterno',
            'categoria_catastale',
            'domus_score',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class PropertyCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating properties"""
    
    class Meta:
        model = Property
        fields = [
            'company',
            'indirizzo',
            'comune',
            'provincia',
            'foglio',
            'particella',
            'subalterno',
            'categoria_catastale',
            'domus_score',
            'status',
        ]
