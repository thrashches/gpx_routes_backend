from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers.user_serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from users.models import User, Follow
from rest_framework import viewsets, status, filters


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "nickname"

    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "nickname"]
    serializer_action_classes = {
        "create": UserCreateSerializer,
        "me": UserUpdateSerializer,
    }

    email_param = openapi.Parameter(
        "email",
        openapi.IN_QUERY,
        description="Email for filtering",
        type=openapi.TYPE_STRING,
    )
    nickname_param = openapi.Parameter(
        "nickname",
        openapi.IN_QUERY,
        description="Nickname for filtering",
        type=openapi.TYPE_STRING,
    )

    common_params = [email_param, nickname_param]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, UserSerializer)

    def get_permissions(self):
        if self.action in ["subscribe", "unsubscribe"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    @swagger_auto_schema(manual_parameters=common_params)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request, *args, **kwargs):
        if request.method == "GET":
            self.object = get_object_or_404(User, pk=request.user.pk)
            serializer = self.get_serializer(self.object)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            serializer = UserUpdateSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["POST"], url_path="subscribe")
    def subscribe(self, request, nickname=None):
        user_to_follow = self.get_object()
        follower = request.user

        if user_to_follow == follower:
            return Response(
                {"error": "You can't subscribe yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        existing_follow = Follow.objects.filter(
            follower=follower, followee=user_to_follow
        ).first()
        if existing_follow:
            return Response(
                {"error": "Already following"}, status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(follower=follower, followee=user_to_follow)
        return Response(
            {"success": f"Subscribed to {user_to_follow.nickname}"},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["POST"], url_path="unsubscribe")
    def unsubscribe(self, request, nickname=None):
        user_to_unfollow = self.get_object()
        follower = request.user

        if user_to_unfollow == follower:
            return Response(
                {"error": "You can't unsubscribe yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            follow_relation = Follow.objects.get(
                follower=follower,
                followee=user_to_unfollow,
            )
        except ObjectDoesNotExist:
            return Response(
                {"error": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow_relation.delete()

        return Response({"success": f"Unsubscribed from {user_to_unfollow.nickname}"})
