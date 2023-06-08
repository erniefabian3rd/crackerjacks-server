from django.db import models

class UserTrip(models.Model):
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="trips")
    trip = models.ForeignKey("Trip", on_delete=models.CASCADE, related_name="users_signed_up")