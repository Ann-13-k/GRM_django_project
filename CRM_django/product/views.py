from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.response import Response

from .models import Product
from storage.models import Storage
from .serializers import ProductSerializer

# Создание продукта
@extend_schema(
        request=ProductSerializer,
        responses={200: ProductSerializer},
        tags=['product'],
        description="Создание продукта (только пользователи компании)"
)
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        storage_id = self.request.data.get('storage')
        storage = get_object_or_404(Storage, id=storage_id)

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        if storage.company != user.company:
            raise PermissionDenied("Склад не принадлежит вашей компании")
        serializer.save(storage=storage)


# Просмотр продукта
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продукта'
                             ),
        ],
        responses={200: ProductSerializer},
        tags=['product'],
        description="Просмотр продукта (доступен пользователям компании)"
)
class ProductDetailView(RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")
        if product.storage.company != user.company:
            raise PermissionDenied("Товар не принадлежит вашей компании")

        return product


# Обновление данных продукта
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продукта'
                             ),
        ],
        responses={200: ProductSerializer},
        tags=['product'],
        description="Обновление данных продукта (доступен пользователям компании)"
)
class ProductUpdateView(UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if product.storage.company != user.company:
            raise PermissionDenied("Товар не принадлежит вашей компании")

        return product


# Удаление продукта
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продукта'
                             ),
        ],
        responses={204: None},
        tags=['product'],
        description="Удаление продукта (только владелец компании)"
)
class ProductDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        product = get_object_or_404(Product, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if product.storage.company != user.company:
            raise PermissionDenied("Товар не принадлежит вашей компании")

        return product

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Продукт {instance.title} удалён"},
            status=status.HTTP_200_OK
        )


# Список продукта
@extend_schema(
    responses={200: ProductSerializer(many=True)},
    tags=['product'],
    description="Список всех продукта вашей компании (доступно всем сотрудникам компании)"
)
class ProductListView(ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        storage_id = self.request.query_params.get('storage')

        if storage_id:
            storage = get_object_or_404(Storage, id=storage_id)
            if storage.company != user.company:
                raise PermissionDenied("Вы не привязаны к компании")
            return Product.objects.filter(storage=storage)
        return Product.objects.filter(storage__company=user.company)

