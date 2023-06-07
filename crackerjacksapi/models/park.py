from django.db import models

class Park(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    image_url = models.TextField(null=True, blank=True)
    capacity = models.CharField(max_length=50)