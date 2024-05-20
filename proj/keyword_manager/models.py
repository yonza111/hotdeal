from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.text