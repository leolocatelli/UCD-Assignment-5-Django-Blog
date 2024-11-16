from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    PostListView,  # Corrigido para usar 'PostListView'
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,  # Corrigido para incluir a classe UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),  # Corrigido aqui também
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),  # Corrigido aqui
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),  # Nova URL para likes
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)