from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.response import Response

from .models import Supplier
from .serializers import SupplierSerializer

# Создание поставщика
@extend_schema(
        request=SupplierSerializer,
        responses={200: SupplierSerializer},
        tags=['supplier'],
        description="Создание поставщика (только владелец компании)"
)
class SupplierCreateView(generics.CreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")
        serializer.save(company=user.company)


# Просмотр поставщика
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID поставщика'
                             ),
        ],
        responses={200: SupplierSerializer},
        tags=['supplier'],
        description="Просмотр поставщика (доступен пользователям компании)"
)
class SupplierDetailView(RetrieveAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])

        if not user.company or supplier.company != user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        return supplier


# Обновление данных поставщика
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID поставщика'
                             ),
        ],
        responses={200: SupplierSerializer},
        tags=['supplier'],
        description="Обновление данных поставщика (доступен пользователям компании)"
)
class SupplierUpdateView(UpdateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])

        if not user.company or supplier.company != user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return supplier


# Удаление поставщика
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID поставщика'
                             ),
        ],
        responses={204: None},
        tags=['supplier'],
        description="Удаление поставщика (только владелец компании)"
)
class SupplierDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        supplier = get_object_or_404(Supplier, pk=self.kwargs['pk'])

        if not user.company or supplier.company != user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return supplier

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Поставщик {instance.title} удалён"},
            status=status.HTTP_200_OK
        )

# Список поставщиков
@extend_schema(
        responses={200: SupplierSerializer(many=True)},
        tags=['supplier'],
        description="Список всех поставщиков вашей компании (доступно всем сотрудникам компании)"
)
class SupplierListView(ListAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")
        return Supplier.objects.filter(company=user.company)
        