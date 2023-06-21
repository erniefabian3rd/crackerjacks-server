from django.db import models

class Trip(models.Model):
    organizer = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="trips")
    title = models.CharField(max_length=100)
    image_url = models.TextField(null=True, blank=True)
    date = models.DateField(null=False, blank=False, auto_now=False, auto_now_add=False)
    location = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    published_date = models.DateTimeField(null=False, blank=False, auto_now=False, auto_now_add=True)
    attendees = models.ManyToManyField("CrackerjacksUser", related_name="attending")

    @property
    def may_edit_or_delete(self):
        return self.__may_edit_or_delete

    @may_edit_or_delete.setter
    def may_edit_or_delete(self, value):
        self.__may_edit_or_delete = value

    @property
    def is_joined(self):
        return self.__is_joined

    @is_joined.setter
    def is_joined(self, value):
        self.__is_joined = value

    def is_joined_by_user(self, user):
        return self.attendees.filter(id=user.id).exists()
    
    @property
    def guest_count(self):
        return self.__guest_count

    @guest_count.setter
    def guest_count(self, value):
        self.__guest_count = value