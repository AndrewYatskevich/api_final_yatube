from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter

from posts.models import Post, Group, Comment, Follow, User

from .serializers import (PostSerializer, GroupSerializer, CommentSerializer,
                          FollowSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_destroy(instance)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        queryset = Comment.objects.filter(post_id=post_id)
        return queryset

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_id')
        )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter, )
    search_fields = ('following__username', )

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Follow.objects.filter(user=user_id)
        return queryset

    def perform_create(self, serializer):
        username = self.request.POST.get('following')
        try:
            serializer.save(
                user=self.request.user,
                following=User.objects.get(username=username)
            )
        except User.DoesNotExist:
            raise ValidationError('Неверное имя пользователя')
        except IntegrityError:
            raise ValidationError('Нельзя подписаться на себя')
