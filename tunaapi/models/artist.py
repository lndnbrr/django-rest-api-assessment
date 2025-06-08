from django.db import models

class Artist (models.Model):
    name = models.CharField(max_length=60)
    age = models.IntegerField()
    bio = models.CharField(max_length=200)
