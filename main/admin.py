from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Patient, Report, ReportSection

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Fields', {'fields': ('cin', 'role', 'is_archived')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Fields', {'fields': ('cin', 'role')}),
    )
    list_display = ['username', 'first_name', 'last_name', 'role', 'is_archived', 'date_joined']
    list_filter = ['role', 'is_archived', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'cin', 'email']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'cin', 'mail', 'reference_dossier', 'date_added', 'added_by']
    list_filter = ['date_added', 'added_by']
    search_fields = ['nom', 'prenom', 'cin', 'mail', 'reference_dossier']
    readonly_fields = ['date_added']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'status', 'date_created', 'created_by', 'validated_by']
    list_filter = ['status', 'date_created', 'created_by', 'validated_by']
    search_fields = ['patient__nom', 'patient__prenom', 'patient__cin', 'text']
    readonly_fields = ['date_created', 'date_modified']

@admin.register(ReportSection)
class ReportSectionAdmin(admin.ModelAdmin):
    list_display = ['report', 'section_title', 'is_accepted', 'order']
    list_filter = ['is_accepted', 'report__status']
    search_fields = ['section_title', 'section_text']
