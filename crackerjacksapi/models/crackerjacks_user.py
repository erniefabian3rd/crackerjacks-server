from django.db import models
from django.contrib.auth.models import User

class CrackerjacksUser(models.Model):
    bio = models.CharField(max_length=255)
    profile_image_url = models.TextField(null=True, blank=True)
    created_on = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=True)
    favorite_team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="user_teams")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_followed(self):
        return self.__is_followed

    @is_followed.setter
    def is_followed(self, value):
        self.__is_followed = value

    def is_followed_by_user(self, user):
        return self.followed_by.filter(follower=user.id).exists()