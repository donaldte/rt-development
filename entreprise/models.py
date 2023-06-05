from django.db import models

from django.contrib.auth.models import User
from django.db import models


class Infrastructure(models.Model):
    nom = models.CharField(max_length=100)
    responsable = models.OneToOneField('Employe', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    structure = models.ForeignKey(Infrastructure, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Machine(models.Model):
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

    nom = models.CharField(max_length=100)
    utilisateur = models.OneToOneField(Employe, on_delete=models.CASCADE)
    description = models.TextField()
    type_machine = models.CharField(max_length=100, choices=TYPE_CHOICES)
    statut = models.CharField(max_length=100, choices=STATUT_CHOICES)
    date_creation = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='machine_images/')  # Chemin de stockage des images

    # Autres détails de la machine selon vos besoins

    def __str__(self):
        return self.nom


class MiseAJour(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    effectue_par = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_mise_a_jour = models.DateField(auto_now_add=True)


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, null=True)
    description = models.TextField(null=True)
    effectuee_par = models.ForeignKey(Employe, on_delete=models.CASCADE)
    date_maintenance = models.DateField()


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=Machine)
def create_mise_a_jour(sender, instance, created, **kwargs):
    if created:
        # Ne crée une nouvelle MiseAJour que si l'objet Machine est nouvellement créé
        MiseAJour.objects.create(machine=instance, effectue_par=instance.utilisateur,
                                 date_mise_a_jour=instance.date_creation)
    else:
        # Met à jour la MiseAJour existante avec les nouvelles informations
        mise_a_jour, _ = MiseAJour.objects.get_or_create(machine=instance, effectue_par=instance.utilisateur,
                                                      date_mise_a_jour=instance.date_creation)
        obj = Machine.objects.get(id=1)
        mise_a_jour.effectue_par = instance.utilisateur.structure.responsable.user.employe
        mise_a_jour.date_mise_a_jour = timezone.now()
        mise_a_jour.save()
