from django.db import models

class Message(models.Model):
    receiver = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey("CrackerjacksUser", on_delete=models.CASCADE, related_name="messages")
    message = models.CharField(max_length=255)
    published_date = models.DateTimeField(null=False, blank=False, auto_now=False, auto_now_add=True)