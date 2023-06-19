from django.db import models

class Division(models.Model):
    name = models.CharField(max_length=100)