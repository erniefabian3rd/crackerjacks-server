from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=255)
    image_url = models.TextField(null=True, blank=True)
    park = models.OneToOneField("Park", on_delete=models.CASCADE)