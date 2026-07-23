from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company, Property


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'nome', 'cognome', 'ruolo', 'stato', 'is_staff', 'created_at')
    list_filter = ('ruolo', 'stato', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nome', 'cognome')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Anagrafica', {'fields': ('nome', 'cognome', 'telefono')}),
        ('Ruolo e stato', {'fields': ('ruolo', 'stato')}),
        ('Permessi', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'cognome', 'password1', 'password2', 'ruolo'),
        }),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('ragione_sociale', 'partita_iva', 'tipo_cliente', 'email', 'created_at')
    list_filter = ('tipo_cliente',)
    search_fields = ('ragione_sociale', 'partita_iva', 'email')
    ordering = ('-created_at',)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('indirizzo', 'comune', 'provincia', 'company', 'domus_score', 'status', 'created_at')
    list_filter = ('status', 'provincia')
    search_fields = ('indirizzo', 'comune', 'foglio', 'particella')
    ordering = ('-created_at',)
    raw_id_fields = ('company',)
