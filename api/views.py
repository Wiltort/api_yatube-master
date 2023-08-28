from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission

class OwnPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE'):
            return request.user == obj.author
        return True


# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, OwnPostPermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['GET'], detail=False)
    def comments(self, request, pk):
        post = get_object_or_404(Post,id=pk)
        comments = post.comments.all()
        return Response(CommentSerializer(comments, many=True).data)

    @action(methods=['DELETE'], detail=False)
    def delete_comment(self, request, pk, comment_pk):
        comment = Comment.objects.get(id=comment_pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=HTTPStatus.NO_CONTENT)

    @action(methods=['GET'], detail=True)
    def view_comment(self, request, pk, comment_pk):
        comment = Comment.objects.get(id=comment_pk)
        return Response(CommentSerializer(comment).data)

    @action(methods=['POST'],detail=True)
    def create_comment(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    @action(methods=['PATCH', 'PUT'], detail=True)
    def update_comment(self, request, pk, comment_pk):
        post = get_object_or_404(Post, id=pk)
        comment = get_object_or_404(Comment, post=post, id=comment_pk)
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)



