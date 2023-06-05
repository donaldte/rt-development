from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('employes/', views.liste_employes, name='employe_list'),
    path('employes/ajouter/', views.ajouter_employe, name='employe_create'),
    path('employes/modifier/<int:employe_id>/', views.modifier_employe, name='employe_update'),
    path('employes/supprimer/<int:employe_id>/', views.supprimer_employe, name='employe_delete'),
    path('machines/', views.liste_machines, name='liste_machines'),
    path('machines/ajouter/', views.ajouter_machine, name='ajouter_machine'),
    path('machines/modifier/<int:machine_id>/', views.modifier_machine, name='modifier_machine'),
    path('machines/supprimer/<int:machine_id>/', views.supprimer_machine, name='supprimer_machine'),
    path('machines/detail/<int:machine_id>/', views.detail_machine, name='detail_machine'),
    path('maintenance/', views.liste_maintenance, name='liste_maintenance'),
    path('miseajour/', views.liste_mise_a_jour, name='liste_miseajour'),
    path('maintenance/ajouter/', views.ajouter_maintenance, name='ajouter_maintenance'),
    path('maintenance/modifier/<int:maintenance_id>/', views.modifier_maintenance, name='modifier_maintenance'),
    path('maintenance/supprimer/<int:maintenance_id>/', views.supprimer_maintenance, name='supprimer_maintenance'),
]
