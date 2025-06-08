from django.http import HttpResponseServerError 
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from tunaapi.models import Song, Artist, Genre
from tunaapi.views.genre_view import GenreSerializer

class SongViewSet(ViewSet):
  
  def retrieve(self, request, pk):
    song = Song.objects.get(pk=pk)
    serialized = SingleSongSerializer(song)
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    songs = Song.objects.all()
    
    serialized = SongSerializer(songs, many="True")
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    artist = Artist.objects.get(pk=request.data["artist_id"])
    song = Song.objects.create(
      title = request.data["title"],
      album = request.data["album"],
      artist = artist,
      length = request.data["length"]
    )
    
    serialized = SongSerializer(song)
    
    return Response(serialized.data, status= status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    song = Song.objects.get(pk=pk)
    song.title = request.data["title"]
    song.album = request.data["album"]
    song.artist = Artist.objects.get(pk = request.data["artist_id"])
    song.length = request.data["length"]
    
    song.save()
    
    serialized = SongSerializer(song)
    
    return Response(serialized.data, status= status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    song = Song.objects.get(pk=pk)
    song.delete()
    return Response(None, status = status.HTTP_204_NO_CONTENT)
    

class SongSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Song
    fields = ('id','title', 'artist_id', 'album', 'length')


class SingleSongSerializer(serializers.ModelSerializer):
  
  genres = serializers.SerializerMethodField()
  
  def get_genres (self, obj):
    genres = Genre.objects.filter(songgenre__song=obj)
    return GenreSerializer(genres, many=True).data
  
  class Meta:
    model = Song
    fields = ('id','title', 'album', 'artist', 'length', 'genres')
    depth = 1
