from django.db import models

class Conductor(models.Model):
    codigo = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    emergencyPhone = models.CharField(max_length=100)
    fullName = models.CharField(max_length=100)
    patentNumber = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    horario_inicio = models.TimeField(null=True, blank=True)
    horario_fin = models.TimeField(null=True, blank=True)
    ruta = models.CharField(max_length=100, blank=True)
