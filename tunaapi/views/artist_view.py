from django.http import HttpResponseServerError 
from tunaapi.models import Artist, Song
from tunaapi.views.song_view import SongSerializer
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response

class ArtistViewSet (ViewSet):
  
  def retrieve(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    songs = Song.objects.filter(artist = artist)
    artist.song_count = songs.count()
    artist.songs.set(songs)
    serialized = SingleArtistSerializer(artist)
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    artists = Artist.objects.all()
    serialized = ArtistSerializer(artists, many="True")
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    
    artist = Artist.objects.create(
      name = request.data["name"],
      age = request.data["age"],
      bio = request.data["bio"],
    )
    
    serialized = ArtistSerializer(artist)
    return Response(serialized.data, status= status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    
    artist.name = request.data["name"]
    artist.age = request.data["age"]
    artist.bio = request.data["bio"]
    
    artist.save()
    
    serialized = ArtistSerializer(artist)
    
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    artist = Artist.objects.get(pk=pk)
    
    artist.delete()
    
    return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer (serializers.ModelSerializer) :
  
  class Meta:
    model = Artist
    fields = ('id','name', 'age', 'bio')
    

class SingleArtistSerializer (serializers.ModelSerializer) :
  
  song_count = serializers.IntegerField(max_value=None, min_value=None)
  songs = SongSerializer(many = True, read_only = True)

  class Meta:
    model = Artist
    fields = ('id','name', 'age', 'bio', 'song_count', 'songs')
    depth = 1
