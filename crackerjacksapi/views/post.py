from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Post, CrackerjacksUser
from rest_framework.decorators import action


class PostView(ViewSet):
    """Post view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        posts = Post.objects.all()
        author = CrackerjacksUser.objects.get(user=request.auth.user)

        for post in posts:
            if post.author == author:
                post.may_edit_or_delete = True
            else:
                post.may_edit_or_delete = False

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST operations to create a post

        Returns
            Response -- JSON serialized post instance
        """
        author = CrackerjacksUser.objects.get(user=request.auth.user)

        post = Post.objects.create(
            image_url=request.data["image_url"],
            caption=request.data["caption"],
            author=author
        )
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        author = CrackerjacksUser.objects.get(user=request.auth.user)
        post.image_url = request.data["image_url"]
        post.caption = request.data["caption"]
        post.author = author

        post.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'image_url', 'caption', 'published_date', 'author', 'may_edit_or_delete')
        depth = 2
