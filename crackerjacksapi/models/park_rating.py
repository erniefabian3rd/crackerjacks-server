from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class ParkRating(models.Model):
    rating_choices = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],choices=rating_choices)
    park = models.ForeignKey("Park", on_delete=models.CASCADE, related_name="park_rating")
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="rating_of_parks")