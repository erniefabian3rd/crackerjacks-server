from django.db import models

class ParkReview(models.Model):
    review = models.CharField(max_length=255)
    park = models.ForeignKey("Park", on_delete=models.CASCADE, related_name="park_reviews")
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="review_of_parks")