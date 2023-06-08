from django.db import models

class Follower(models.Model):
    follower = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="following")
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="followed_by")
    followed_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)