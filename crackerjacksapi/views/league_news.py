from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import LeagueNews
from rest_framework.decorators import action


class LeagueNewsView(ViewSet):
    """League News view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single article

        Returns:
            Response -- JSON serialized article"""

        article = LeagueNews.objects.get(pk=pk)
        serializer = LeagueNewsSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all articles

        Returns:
            Response -- JSON serialized list of articles"""

        articles = LeagueNews.objects.all()
        serializer = LeagueNewsSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LeagueNewsSerializer(serializers.ModelSerializer):
    """JSON serializer for league news"""
    class Meta:
        model = LeagueNews
        fields = ('id', 'title', 'article', 'link_url', 'published_date')