from django.db import models

class PostLike(models.Model):
    user = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="user_likes")