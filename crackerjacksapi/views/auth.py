from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from crackerjacksapi.models import CrackerjacksUser, Team

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a Crackerjacks user

    Method arguments:
        request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new Crackerjacks user for authentication

    Method arguments:
        request -- The full HTTP request object
    '''
    favorite_team = Team.objects.get(pk=request.data["favorite_team"])

    new_user = User.objects.create_user(
        username=request.data['username'],
        password=request.data['password'],
        email=request.data['email'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    crackerjacks_user = CrackerjacksUser.objects.create(
        bio=request.data['bio'],
        profile_image_url=request.data['profile_image_url'],
        favorite_team=favorite_team,
        user=new_user
    )

    token = Token.objects.create(user=crackerjacks_user.user)
    data = { 'token': token.key }
    return Response(data)
