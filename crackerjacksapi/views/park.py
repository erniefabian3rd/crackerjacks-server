from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Park, CrackerjacksUser, UserVisitedPark
from rest_framework.decorators import action


class ParkView(ViewSet):
    """Park view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single park

        Returns:
            Response -- JSON serialized park
        """
        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        park = Park.objects.get(pk=pk)
        visited_parks = UserVisitedPark.objects.all()

        for parks in visited_parks:
            if parks.user == cj_user and parks.park == park:
                park.is_visited = True
            else:
                park.is_visited = False

        serializer = ParkSerializer(park)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all parks

        Returns:
            Response -- JSON serialized list of parks
        """
        parks = Park.objects.all()
        serializer = ParkSerializer(parks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=True)
    def visited(self, request, pk):
        """Post request for a user to mark a park as visited"""

        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        park = Park.objects.get(pk=pk)

        visited_park = UserVisitedPark.objects.create(
            user = cj_user,
            park = park
        )
        serializer = UserVisitedParkSerializer(visited_park)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['DELETE'], detail=True)
    def unvisited(self, request, pk):
        """Delete request for a user to mark a park as not visited"""

        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        park = Park.objects.get(pk=pk)
        visited_park = UserVisitedPark.objects.get(user=cj_user, park=park)

        visited_park.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ParkSerializer(serializers.ModelSerializer):
    """JSON serializer for parks"""
    class Meta:
        model = Park
        fields = ('id', 'name', 'bio', 'location', 'image_url', 'capacity', 'rating', 'review', 'home_team', 'users_visited', 'is_visited')
        depth = 1

class UserVisitedParkSerializer(serializers.ModelSerializer):
    """JSON serializer for visited_parks"""
    class Meta:
        model = UserVisitedPark
        fields = ('id', 'user', 'park')
        depth = 1
