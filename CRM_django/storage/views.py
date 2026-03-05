from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .models import Storage
from .serializers import StorageSerializer

# Создание склада
@extend_schema(
        request=StorageSerializer,
        responses={200: StorageSerializer},
        tags=['storage'],
        description="Создание склада (только владелец компании)"
)
class StorageCreateView(generics.CreateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, 'company') or not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")
        serializer.save(company=user.company)

# Просмотр склада
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID склада'
                             ),
        ],
        responses={200: StorageSerializer},
        tags=['storage'],
        description="Просмотр склада (доступен пользователям компании)"
)
class StorageDetailView(RetrieveAPIView):
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        storage = get_object_or_404(Storage, pk=self.kwargs['pk'])

        if not hasattr(user, 'company') or storage.company != user.company:
            raise PermissionDenied("Вы не можете посмотреть данные чужой компании")

        return storage

# Обновление данных склада
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID склада'
                             ),
        ],
        responses={200: StorageSerializer},
        tags=['storage'],
        description="Обновление данных склада (доступен пользователям компании)"
)
class StorageUpdateView(UpdateAPIView):
    serializer_class = StorageSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user
        storage = get_object_or_404(Storage, pk=self.kwargs['pk'])

        if not hasattr(user, 'company') or storage.company != user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return storage

# Удаление склада
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID склада'
                             ),
        ],
        responses={204: None},
        tags=['storage'],
        description="Удаление склада (только владелец компании)"
)
class StorageDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        storage = get_object_or_404(Storage, pk=self.kwargs['pk'])

        if not hasattr(user, 'company') or storage.company != user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return storage