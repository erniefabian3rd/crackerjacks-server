from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Comment, CrackerjacksUser, Post
from rest_framework.decorators import action


class CommentView(ViewSet):
    """Comment view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment"""

        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all comments

        Returns:
            Response -- JSON serialized list of comments"""

        comments = Comment.objects.all()
        post_id = request.query_params.get('post', None)

        if post_id is not None:
            comments = comments.filter(post_id=post_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST request for comment"""

        author = CrackerjacksUser.objects.get(user=request.auth.user)
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a comment

        Returns:
            Response -- Empty body with 204 status code"""

        post = Post.objects.get(pk=pk)
        author = CrackerjacksUser.objects.get(user=request.auth.user)
        comment = Comment.objects.get(pk=pk)

        comment.comment = request.data["comment"]
        comment.post = post
        comment.author = author

        comment.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        comment.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for posts"""
    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'comment', 'published_date')
        depth = 2

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'post', 'comment', 'published_date')
