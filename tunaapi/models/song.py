from django.db import models
from .artist import Artist

class Song (models.Model):
    title = models.CharField(max_length=100)
    album = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    length = models.IntegerField()
