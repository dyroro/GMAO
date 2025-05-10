from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

################# model de table : monapp_notification ########################
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    message = models.TextField()
    date = models.DateTimeField()
    is_read = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # champ = user (et non for_user)

    def __str__(self):
        return f"{self.user.username} : {self.message}"


########### model de table : monapp_Equipment #################################

class Equipment(models.Model):
    CRITICITE_CHOICES = [
        ('haut', 'Haut'),
        ('moyenne', 'Moyenne'),
        ('faible', 'Faible')
    ]
    TYPE_MAINT = [
        ('corrective', 'Corrective'),
        ('paliative', 'Paliative'),
        ('preventive', 'Preventive')
    ]
    N = models.AutoField(primary_key=True)
    IDD = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    criticite= models.CharField(max_length=20, choices=CRITICITE_CHOICES)
    type_maint=models.CharField(max_length=20, choices=TYPE_MAINT)
    nombre=models.IntegerField()
    date_maint = models.DateField()


    def __str__(self):
        return self.name
########### model de table : monapp_personnel #################################

class Personnel(models.Model):
    N = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)

########### model de table : monapp_historiqueplanning ########################

from django.db import models

class HistoriquePlanning(models.Model):
    N = models.AutoField(primary_key=True)
    type = models.CharField(max_length=200)
    duree = models.IntegerField()
    jour = models.IntegerField()
    mois = models.IntegerField()
    ans = models.IntegerField()

########### model de table : monapp_Historique_de_pannes ######################

from django.utils.translation import gettext_lazy as _
class Historique_de_pannes(models.Model):
    class CriticiteChoices(models.TextChoices):
        LOW = 'L', _('Faible')
        MEDIUM = 'M', _('Moyenne')
        HIGH = 'H', _('Haute')

    id = models.AutoField(primary_key=True)
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        verbose_name=_("Équipement"),
        related_name='pannes'
    )
    panne = models.TextField(_("Description de la panne"))
    ttr = models.IntegerField()
    criticite = models.CharField(
        _("Criticité"),
        max_length=1,
        choices=CriticiteChoices.choices,
        default=CriticiteChoices.MEDIUM
    )
    agent = models.CharField(_("Agent responsable"), max_length=100)
    annee_panne = models.PositiveIntegerField(
        _("Année de panne"),
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)
        ]
    )
########### model de table : monapp_Historique_de_PDR #########################

class Historique_de_PDR(models.Model):
    N = models.AutoField(primary_key=True)
    ID =models.CharField()
    PDR = models.CharField()
    fournisseur=models.CharField()
    date_commande=models.DateField()
    date_livraison=models.DateField()
    consomation=models.IntegerField()
    ans = models.IntegerField()
    equipement = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='pdrs'
    )
########### model de table : monapp_bontravail #########################
from django.db import models

class BonTravail(models.Model):
    numero = models.CharField(max_length=100)
    date = models.DateField()
    demandeur = models.CharField(max_length=100)
    lieu = models.CharField(max_length=200)
    description = models.TextField()
    technicien = models.CharField(max_length=100)
    duree = models.CharField(max_length=50)

    def __str__(self):
        return f"Bon {self.numero}"

