from django.http import HttpResponseServerError 
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from rest_framework.response import Response
from tunaapi.models import Genre, Song


class GenreViewSet(ViewSet):
  
  def retrieve(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    serialized = SingleGenreSerializer(genre)
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def list(self, request):
    genres = Genre.objects.all()
    serialized = GenreSerializer(genres, many="True")
    return Response(serialized.data, status=status.HTTP_200_OK)
  
  def create(self, request):
    genre = Genre.objects.create(
      description = request.data["description"]
    )
    
    serialized = GenreSerializer(genre)
    
    return Response(serialized.data, status= status.HTTP_201_CREATED)
  
  def update(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.description = request.data["description"]
    
    genre.save()
    
    serialized = GenreSerializer(genre)
    
    return Response(serialized.data, status= status.HTTP_200_OK)
  
  def destroy(self, request, pk):
    genre = Genre.objects.get(pk=pk)
    
    genre.delete()
    
    return Response(None, status = status.HTTP_204_NO_CONTENT)

class GenreSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Genre
    fields = ('id','description')
    
class SingleGenreSerializer(serializers.ModelSerializer):
  
  songs = serializers.SerializerMethodField()
  
  def get_songs(self, obj):
    from tunaapi.views.song_view import SongSerializer
    songs = Song.objects.filter(songgenre__genre = obj)
    return SongSerializer(songs, many=True).data
    
  class Meta:
    model = Genre
    fields = ('id','description', 'songs')
