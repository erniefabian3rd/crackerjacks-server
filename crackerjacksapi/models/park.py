from django.db import models

class Park(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    image_url = models.TextField(null=True, blank=True)
    capacity = models.CharField(max_length=50)
    rating = models.ManyToManyField("CrackerjacksUser", through="ParkRating", related_name="park_ratings")
    review = models.ManyToManyField("CrackerjacksUser", through="ParkReview", related_name="park_reviews")

    @property
    def is_visited(self):
        return self.__is_visited

    @is_visited.setter
    def is_visited(self, value):
        self.__is_visited = value