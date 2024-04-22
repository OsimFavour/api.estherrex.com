from rest_framework import generics
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import (
    IsAdminUser, BasePermission, 
    DjangoModelPermissions, SAFE_METHODS,
    IsAuthenticatedOrReadOnly)

class PostUserWritePermission(BasePermission):
    """
    The user of the particular post is the only 
    person that can re-write or delete
    """
    message = 'Editing Posts is restricted to the author only'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True
        
        return obj.author == request.user

class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer