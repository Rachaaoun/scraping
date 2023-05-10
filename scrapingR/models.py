from django.db import models

# Create your models here.

class annonce(models.Model):
    ANNONCE_LINK = models.CharField(max_length=255)
    ANNONCE_ID = models.IntegerField()
    FROM_SITE = models.CharField(max_length=255)
    ANNONCE_DATE = models.CharField(max_length=255)
    TYPE = models.CharField(max_length=255)
    NOM = models.CharField(max_length=255)
    ADRESSE = models.CharField(max_length=255)
    CP = models.CharField(max_length=255)
    VILLE = models.CharField(max_length=255)
    ANNONCE_TEXT = models.CharField(max_length=255)
    NB_ETAGE = models.IntegerField()
    SURFACE_TOTAL = models.IntegerField()
    SURFACE_HABITABLE = models.IntegerField()
    NB_VOITURE = models.IntegerField()
    NB_PIECE = models.IntegerField()
    PRIX = models.CharField(max_length=255)
    ANNEE_CONSTRUCTION = models.CharField(max_length=255)