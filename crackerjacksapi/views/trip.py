from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Trip, CrackerjacksUser


class TripView(ViewSet):
    """Trip view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        trip = Trip.objects.get(pk=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips
        """
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations to create a trip

        Returns
            Response -- JSON serialized trip instance
        """
        organizer = CrackerjacksUser.objects.get(user=request.auth.user)

        trip = Trip.objects.create(
            title=request.data["title"],
            image_url=request.data["image_url"],
            date=request.data["date"],
            location=request.data["location"],
            details=request.data["details"],
            organizer=organizer
        )
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a trip

        Returns:
            Response -- Empty body with 204 status code
        """

        trip = Trip.objects.get(pk=pk)
        organizer = CrackerjacksUser.objects.get(user=request.auth.user)
        trip.title = request.data["title"]
        trip.image_url = request.data["image_url"]
        trip.date = request.data["date"]
        trip.location = request.data["location"]
        trip.details = request.data["details"]
        trip.organizer = organizer

        trip.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        trip.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for trips
    """
    class Meta:
        model = Trip
        fields = ('id', 'organizer', 'title', 'image_url', 'date', 'location', 'details', 'published_date')
        depth = 2
