from django.db import models
from django.contrib.auth import get_user_model


class UploadTemplate(models.Model):
    name = models.CharField(max_length=20)
    event_name = models.CharField(max_length=20)
    file = models.TextField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "{} for {}".format(self.name, self.event_name)


