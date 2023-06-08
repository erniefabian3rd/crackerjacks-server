from django.db import models

class UserVisitedPark(models.Model):
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="visited_parks")
    park = models.ForeignKey("Park", on_delete=models.CASCADE, related_name="users_visited")