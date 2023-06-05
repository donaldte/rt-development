from django.contrib import admin
from .models import Employe, Machine, Infrastructure, MiseAJour, Maintenance


@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'utilisateur', 'type_machine', 'statut')


@admin.register(Infrastructure)
class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'responsable')


@admin.register(MiseAJour)
class MiseAJourAdmin(admin.ModelAdmin):
    list_display = ('machine', 'effectue_par', 'date_mise_a_jour')


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'effectuee_par', 'description', 'date_maintenance')
