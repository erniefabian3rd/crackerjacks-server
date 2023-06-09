from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Trip


class TripView(ViewSet):
    """Trip view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        trip = Trip.objects.get(pk=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    
    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips
        """
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)
    
class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for trips
    """
    class Meta:
        model = Trip
        fields = ('id', 'organizer', 'title', 'image_url', 'date', 'location', 'details', 'published_date')
        depth = 2
