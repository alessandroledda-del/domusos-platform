from django.contrib import admin
from .models import Company, CompanyInvitation, CompanyMembership

admin.site.register(Company)
admin.site.register(CompanyMembership)
admin.site.register(CompanyInvitation)
