from django.db import models

class LeagueNews(models.Model):
    title = models.CharField(max_length=100)
    article = models.CharField(max_length=255)
    published_date = models.CharField(max_length=100)
    link_url = models.TextField(null=True, blank=True)
