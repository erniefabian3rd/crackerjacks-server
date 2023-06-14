from django.db import models

class Trip(models.Model):
    organizer = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="trips")
    title = models.CharField(max_length=100)
    image_url = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    published_date = models.DateTimeField(null=False, blank=False, auto_now=False, auto_now_add=True)

    @property
    def may_edit_or_delete(self):
        return self.__may_edit_or_delete

    @may_edit_or_delete.setter
    def may_edit_or_delete(self, value):
        self.__may_edit_or_delete = value