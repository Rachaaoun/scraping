from django.db import models

# Create your models here.

class Produit(models.Model):
    titre = models.CharField(max_length=100)