from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from crackerjacksapi.models import Post, CrackerjacksUser, PostLike
from rest_framework.decorators import action


class PostView(ViewSet):
    """Post view"""
    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        author = CrackerjacksUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)

        if post.author == author:
            post.may_edit_or_delete = True
        else:
            post.may_edit_or_delete = False

        post.is_liked = post.is_liked_by_user(author)

        post.like_count = len(PostLike.objects.filter(post_id=post))

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        author = CrackerjacksUser.objects.get(user=request.auth.user)
        following = author.following.values_list('user_id', flat=True)
        posts = Post.objects.filter(Q(author__id__in=following) | Q(author=author))

        for post in posts:
            if post.author == author:
                post.may_edit_or_delete = True
            else:
                post.may_edit_or_delete = False

            post.is_liked = post.is_liked_by_user(author)

            search = request.query_params.get('search', None)
            if search is not None:
                posts = posts.filter(
                    Q(author__user__username__icontains=search) |
                    Q(caption__icontains=search)
                )

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
    
    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        """Post request for a user to like a post"""

        user = CrackerjacksUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.like.add(user)
        return Response({'message': 'Post was liked'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['DELETE'], detail=True)
    def unlike(self, request, pk):
        """Delete request for a user to unlike a post"""

        user = CrackerjacksUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.like.remove(user)
        return Response({'message': 'Post was unliked'}, status=status.HTTP_204_NO_CONTENT)
    
class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    class Meta:
        model = Post
        fields = ('id', 'image_url', 'caption', 'published_date', 'author', 'may_edit_or_delete', 'like', 'is_liked', 'like_count')
        depth = 3
