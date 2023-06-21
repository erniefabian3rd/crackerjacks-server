from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Trip, CrackerjacksUser
from rest_framework.decorators import action


class TripView(ViewSet):
    """Trip view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        attendee = CrackerjacksUser.objects.get(user=request.auth.user)
        trip = Trip.objects.get(pk=pk)

        trip.is_joined = trip.is_joined_by_user(attendee)

        trip.guest_count = trip.attendees.count()

        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips
        """
        trips = Trip.objects.all()
        organizer = CrackerjacksUser.objects.get(user=request.auth.user)

        for trip in trips:
            if trip.organizer == organizer:
                trip.may_edit_or_delete = True
            else:
                trip.may_edit_or_delete = False
            
            trip.is_joined = trip.is_joined_by_user(organizer)

            search = request.query_params.get('search', None)
            if search is not None:
                trips = trips.filter(
                    Q(organizer__user__username__icontains=search) |
                    Q(title__icontains=search) |
                    Q(location__icontains=search)
                )


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

    @action(methods=['POST'], detail=True)
    def join(self, request, pk):
        """Post request for a user to join a trip"""

        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        trip = Trip.objects.get(pk=pk)
        trip.attendees.add(cj_user)
        return Response({'message': 'User added to trip'}, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=True)
    def leave(self, request, pk):
        """Delete request for a user to leave a trip"""

        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        trip = Trip.objects.get(pk=pk)
        trip.attendees.remove(cj_user)
        return Response({'message': 'User left the trip'}, status=status.HTTP_204_NO_CONTENT)
    
class TripSerializer(serializers.ModelSerializer):
    """JSON serializer for trips
    """
    class Meta:
        model = Trip
        fields = ('id', 'organizer', 'title', 'image_url', 'date', 'location', 'details', 'published_date', 'may_edit_or_delete', 'attendees', 'is_joined', 'guest_count')
        depth = 2
