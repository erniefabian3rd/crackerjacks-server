from django.db import models

class Post(models.Model):
    author = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="posts_published")
    image_url = models.TextField(null=True, blank=True)
    caption = models.CharField(max_length=255)
    published_date = models.DateTimeField(null=False, blank=False, auto_now=False, auto_now_add=True)
    like = models.ManyToManyField("CrackerjacksUser", through="PostLike", related_name="post_likes")

    @property
    def may_edit_or_delete(self):
        return self.__may_edit_or_delete

    @may_edit_or_delete.setter
    def may_edit_or_delete(self, value):
        self.__may_edit_or_delete = value