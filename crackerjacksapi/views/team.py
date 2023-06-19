from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status, permissions
from crackerjacksapi.models import Team


class TeamView(ViewSet):
    """Team view"""
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, pk):
        """Handle GET requests for single team

        Returns:
            Response -- JSON serialized team
        """
        team = Team.objects.get(pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all teams

        Returns:
            Response -- JSON serialized list of teams
        """
        teams = Team.objects.all()

        search = request.query_params.get('search', None)
        if search is not None:
            teams = teams.filter(
                Q(name__icontains=search) |
                Q(division__name__icontains=search)
            )

        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TeamSerializer(serializers.ModelSerializer):
    """JSON serializer for teams
    """
    class Meta:
        model = Team
        fields = ('id', 'name', 'bio', 'image_url', 'park', 'division')
        depth = 1
