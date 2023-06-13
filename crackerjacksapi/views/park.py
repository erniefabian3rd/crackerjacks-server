from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Park


class ParkView(ViewSet):
    """Park view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single park

        Returns:
            Response -- JSON serialized park
        """
        park = Park.objects.get(pk=pk)
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
    
class ParkSerializer(serializers.ModelSerializer):
    """JSON serializer for parks"""
    class Meta:
        model = Park
        fields = ('id', 'name', 'bio', 'location', 'image_url', 'capacity', 'rating', 'review', 'home_team')
        depth = 1
