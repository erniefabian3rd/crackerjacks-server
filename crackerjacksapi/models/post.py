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

    @property
    def is_liked(self):
        return self.__is_liked

    @is_liked.setter
    def is_liked(self, value):
        self.__is_liked = value

    def is_liked_by_user(self, user):
        return self.like.filter(id=user.id).exists()

    @property
    def like_count(self):
        return self.__like_count

    @like_count.setter
    def like_count(self, value):
        self.__like_count = value