from django.http import HttpResponseServerError 
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from tunaapi.models import SongGenre, Song, Genre

class SongGenreViewSet (ViewSet):
  
  def retrieve(self, request, pk):
    song_genre = SongGenre.objects.get(pk=pk)
    serialized = SongGenreSerializer(song_genre)
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    
    song = Song.objects.get(pk = request.data["song_id"])
    genre = Genre.objects.get(pk = request.data["genre_id"])
    song_genre = SongGenre.objects.create(
      song_id = song.pk,
      genre_id = genre.pk
    )
    serialized = SongGenreSerializer(song_genre)
    return Response(serialized.data, status=status.HTTP_201_CREATED)

class SongGenreSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = SongGenre
    fields = ('id', 'song', 'genre')
    depth = 1
