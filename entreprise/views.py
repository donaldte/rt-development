from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Infrastructure, Employe, MiseAJour
from .forms import EmployeForm, MachineForm, MaintenanceForm
from .models import Machine
from django.contrib import messages
from .models import Maintenance
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    """ Page d'accueil """
    return render(request, 'home.html')


@login_required()
def liste_employes(request):
    try:
        structure = Infrastructure.objects.get(responsable=request.user.employe)
        employes = Employe.objects.filter(structure=structure)
    except Infrastructure.DoesNotExist:
        messages.error(request, "La structure n'existe pas.")
        return redirect('dashboard')
    return render(request, 'liste_employes.html', {'employes': employes})


@login_required()
def ajouter_employe(request):
    try:
        structure = Infrastructure.objects.get(responsable=request.user.employe)
    except Infrastructure.DoesNotExist:
        messages.error(request, "La structure n'existe pas.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.structure = structure
            employe.save()
            messages.success(request, "L'employé a été ajouté avec succès.")
            return redirect('employe_list')
    else:
        form = EmployeForm()
    return render(request, 'ajouter_employe.html', {'form': form})


@login_required()
def modifier_employe(request, employe_id):
    try:
        structure = Infrastructure.objects.get(responsable=request.user.employe)
        employe = get_object_or_404(Employe, id=employe_id, structure=structure)
    except Infrastructure.DoesNotExist:
        messages.error(request, "La structure n'existe pas.")
        return redirect('dashboard')
    except Employe.DoesNotExist:
        messages.error(request, "L'employé n'existe pas.")
        return redirect('employe_list')

    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            messages.success(request, "L'employé a été modifié avec succès.")
            return redirect('employe_list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'modifier_employe.html', {'form': form, 'employe': employe})


@login_required()
def supprimer_employe(request, employe_id):
    try:
        structure = Infrastructure.objects.get(responsable=request.user.employe)
        employe = get_object_or_404(Employe, id=employe_id, structure=structure)
        user = employe.user
        employe.delete()
        user.delete()
        messages.success(request, "L'employé a été supprimé avec succès.")
    except Infrastructure.DoesNotExist:
        messages.error(request, "La structure n'existe pas.")
    except Employe.DoesNotExist:
        messages.error(request, "L'employé n'existe pas.")
    return redirect('employe_list')


@login_required()
def liste_machines(request):
    machines = Machine.objects.filter(utilisateur__structure__responsable=request.user.employe)
    if not machines:
        machines = Machine.objects.filter(utilisateur=request.user.employe)
    return render(request, 'liste_machines.html', {'machines': machines})


@login_required()
def detail_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'detail_machine.html', {'machine': machine})

@login_required()
def ajouter_machine(request):
    if request.method == 'POST':
        form = MachineForm(request.POST, request.FILES)
        if form.is_valid():
            machine = form.save()
            messages.success(request, 'La machine a été ajoutée avec succès.')
            return redirect('liste_machines')
        else:
            messages.error(request, 'Une erreur est survenue. Veuillez vérifier les informations.')
    else:
        form = MachineForm()
    return render(request, 'ajouter_machine.html', {'form': form})

@login_required()
def modifier_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    if request.method == 'POST':
        form = MachineForm(request.POST, request.FILES, instance=machine)
        if form.is_valid():
            form.save()
            messages.success(request, 'La machine a été modifiée avec succès.')
            return redirect('liste_machines')
        else:
            messages.error(request, 'Une erreur est survenue. Veuillez vérifier les informations.')
    else:
        form = MachineForm(instance=machine)
    return render(request, 'modifier_machine.html', {'form': form, 'machine': machine})

@login_required()
def supprimer_machine(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id, utilisateur__structure__responsable=request.user.employe)
    machine.delete()
    messages.success(request, 'La machine a été supprimée avec succès.')
    return redirect('liste_machines')

@login_required()
def liste_maintenance(request):
    maintenances = Maintenance.objects.filter(effectuee_par=request.user.employe)
    return render(request, 'liste_maintenance.html', {'maintenances': maintenances})

@login_required()
def ajouter_maintenance(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.effectuee_par = request.user.employe
            maintenance.save()
            return redirect('liste_maintenance')
    else:
        form = MaintenanceForm()
    return render(request, 'ajouter_maintenance.html', {'form': form})

@login_required()
def modifier_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance)
        if form.is_valid():
            form.save()
            return redirect('liste_maintenance')
    else:
        form = MaintenanceForm(instance=maintenance)
    return render(request, 'modifier_maintenance.html', {'form': form, 'maintenance': maintenance})

@login_required()
def supprimer_maintenance(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    maintenance.delete()
    return redirect('liste_maintenance')

@login_required()   
def liste_mise_a_jour(request):
    mises_a_jour = MiseAJour.objects.all()
    return render(request, 'liste_mise_a_jour.html', {'mises_a_jour': mises_a_jour})
