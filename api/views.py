from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from .serializers import PostSerializer
# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
