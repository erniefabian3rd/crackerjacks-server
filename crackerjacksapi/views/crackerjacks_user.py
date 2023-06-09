from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import CrackerjacksUser, Team, Follower
from django.contrib.auth.models import User
from rest_framework.decorators import action


class CrackerjacksUserView(ViewSet):
    """Crackerjacks user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single cj user

        Returns:
            Response -- JSON serialized cj user
        """
        auth_user = CrackerjacksUser.objects.get(user=request.auth.user)
        cj_user = CrackerjacksUser.objects.get(pk=pk)
        
        cj_user.is_followed = cj_user.is_followed_by_user(auth_user)

        serializer = CrackerjacksUserSerializer(cj_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all cj users

        Returns:
            Response -- JSON serialized list of cj users
        """
        cj_users = CrackerjacksUser.objects.all()

        search = request.query_params.get('search', None)
        if search is not None:
            cj_users = cj_users.filter(
                Q(user__username__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(favorite_team__name__icontains=search)
            )

        serializer = CrackerjacksUserSerializer(cj_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """

        cj_user = CrackerjacksUser.objects.get(pk=pk)
        cj_user.bio = request.data["bio"]
        cj_user.profile_image_url = request.data["profile_image_url"]
        cj_user.favorite_team = Team.objects.get(pk=request.data["favorite_team"])

        cj_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @ action(methods=["get"], detail=False)
    def myprofile(self, request):
        """Get method for my profile"""
        cj_user = CrackerjacksUser.objects.get(user=request.auth.user)

        try:
            serializer = CrackerjacksUserSerializer(cj_user, many=False)
            return Response(serializer.data)
        except CrackerjacksUser.DoesNotExist:
            return Response({"message": "I do not exist."}, status=404)

    @action(methods=['POST'], detail=True)
    def follow(self, request, pk):
        """Post request for a user to follow another user"""

        auth_user = CrackerjacksUser.objects.get(user=request.auth.user)
        other_user = CrackerjacksUser.objects.get(pk=pk)

        follower = Follower.objects.create(
            follower = auth_user,
            user = other_user
        )
        serializer = FollowerSerializer(follower)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(methods=['DELETE'], detail=True)
    def unfollow(self, request, pk):
        """Delete request for a user to unfollow another user"""

        auth_user = CrackerjacksUser.objects.get(user=request.auth.user)
        other_user = CrackerjacksUser.objects.get(pk=pk)
        follower = Follower.objects.get(follower=auth_user, user=other_user)

        follower.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CrackerjacksUserSerializer(serializers.ModelSerializer):
    """JSON serializer for cj users"""
    class Meta:
        model = CrackerjacksUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'favorite_team', 'user', 'post_likes', 'followed_by', 'following', 'is_followed', 'visited_parks')
        depth = 1

class FollowerSerializer(serializers.ModelSerializer):
    """JSON serializer for followers"""
    class Meta:
        model = Follower
        fields = ('id', 'follower', 'user', 'followed_on')
        depth = 1