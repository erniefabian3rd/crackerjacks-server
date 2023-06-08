from django.db import models

class ParkRating(models.Model):
    rating = models.IntegerField()
    park = models.ForeignKey("Park", on_delete=models.CASCADE, related_name="park_rating")
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="rating_of_parks")