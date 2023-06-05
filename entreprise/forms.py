# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Employe, Infrastructure, Machine, Maintenance


class EmployeForm(UserCreationForm):
    first_name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Prenom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    role = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    infrastructure = forms.ModelChoiceField(queryset=Infrastructure.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control'}))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', "last_name", 'email', 'role', 'infrastructure', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.save()

        employe = Employe.objects.create(user=user, role=self.cleaned_data['role'],
                                         structure=self.cleaned_data['infrastructure'])
        return employe


class MachineForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('PC', 'PC'),
        ('Desktop', 'Desktop'),
        ('Switch', 'Switch'),
        ('Serveur', 'Serveur'),
        # Ajoutez d'autres types de machines selon vos besoins
    ]

    STATUT_CHOICES = [
        ('Défaillant', 'Défaillant'),
        ('Bon état', 'Bon état'),
        ('En maintenance', 'En maintenance'),
        # Ajoutez d'autres statuts selon vos besoins
    ]

    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    utilisateur = forms.ModelChoiceField(queryset=Employe.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    type_machine = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    statut = forms.ChoiceField(choices=STATUT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Machine
        fields = ['nom', 'utilisateur', 'description', 'type_machine', 'statut', 'image']


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['machine', 'date_maintenance', 'description']
        widgets = {
            'machine': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'date_maintenance': forms.DateInput(attrs={'class': 'form-control'}),
        }
