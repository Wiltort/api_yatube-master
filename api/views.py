from http import HTTPStatus
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from posts.models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission

class OwnPostPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('PUT', 'PATCH', 'DELETE', 'POST'):
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
        post = Post.objects.get(id=pk)
        comments = post.comments.all()
        return Response(CommentSerializer(comments, many=True).data)

    @action(methods=['DELETE'], detail=False)
    def delete_comment(self, request, pk, comment_pk):
        comment = Comment.objects.get(id=comment_pk)
        self.check_object_permissions(request, comment)
        return Response(status=HTTPStatus.ACCEPTED)




