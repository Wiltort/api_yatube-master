from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .views import PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)

urlpatterns = [
    path('posts/<int:pk>/comments/', PostViewSet.as_view(actions={'get': 'comments', 'post': 'create_comment'})),
    path('posts/<int:pk>/comments/<int:comment_pk>/',
         PostViewSet.as_view(actions={'delete': 'delete_comment', 'get': 'view_comment',
                                      'patch': 'update_comment', 'put': 'update_comment'})),
    path('', include(router.urls)),

]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token),

]
