from django.http import HttpResponseServerError
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Park, CrackerjacksUser, UserVisitedPark, ParkReview, ParkRating
from rest_framework.decorators import action
from django.db.models import Avg

class ParkView(ViewSet):
    """Park view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single park

        Returns:
            Response -- JSON serialized park
        """
        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        park = Park.objects.get(pk=pk)

        visited_park = UserVisitedPark.objects.filter(user=cj_user, park=park).exists()
        park.is_visited = visited_park
        
        avg_rating = ParkRating.objects.filter(park_id = park).aggregate(Avg('rating'))
        park.avg_rating = avg_rating['rating__avg']

        serializer = ParkSerializer(park)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all parks

        Returns:
            Response -- JSON serialized list of parks
        """
        parks = Park.objects.all()

        for park in parks:
            avg_rating = ParkRating.objects.filter(park_id = park).aggregate(Avg('rating'))
            park.avg_rating = avg_rating['rating__avg']

        search = request.query_params.get('search', None)
        if search is not None:
            parks = parks.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search)
            )

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
    
    @action(methods=['POST'], detail=True)
    def review(self, request, pk):
        """Post request for a user to review a park"""

        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)
        park = Park.objects.get(pk=pk)
        review = request.data['review']
        rating = request.data['rating']

        if rating < 1 or rating > 5:
            raise ValidationError({'rating': 'Rating should be between 1 and 5'})

        if ParkReview.objects.filter(user=cj_user, park=park).exists():
            return Response({'message': 'You have already reviewed this park'})
        else:
            ParkReview.objects.create(review = review, user = cj_user, park = park)

        if ParkRating.objects.filter(user=cj_user, park=park).exists():
            return Response({'message': 'You have already rated this park'})
        else:
            ParkRating.objects.create(rating = rating, user = cj_user, park = park)
            return Response({'message': 'Thanks for rating the park!'}, status=status.HTTP_201_CREATED)
    
class ParkSerializer(serializers.ModelSerializer):
    """JSON serializer for parks"""
    class Meta:
        model = Park
        fields = ('id', 'name', 'bio', 'location', 'image_url', 'capacity', 'home_team', 'users_visited', 'is_visited', 'park_rating', 'park_reviews', 'avg_rating')
        depth = 1

class UserVisitedParkSerializer(serializers.ModelSerializer):
    """JSON serializer for visited_parks"""
    class Meta:
        model = UserVisitedPark
        fields = ('id', 'user', 'park')
        depth = 1
