from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import CrackerjacksUser, Team
from django.contrib.auth.models import User
from rest_framework.decorators import action


class CrackerjacksUserView(ViewSet):
    """Crackerjacks user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single cj user

        Returns:
            Response -- JSON serialized cj user
        """
        cj_user = CrackerjacksUser.objects.get(pk=pk)
        serializer = CrackerjacksUserSerializer(cj_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all cj users

        Returns:
            Response -- JSON serialized list of cj users
        """
        cj_users = CrackerjacksUser.objects.all()
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
    
class CrackerjacksUserSerializer(serializers.ModelSerializer):
    """JSON serializer for cj users"""
    class Meta:
        model = CrackerjacksUser
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'favorite_team', 'user')
        depth = 1
