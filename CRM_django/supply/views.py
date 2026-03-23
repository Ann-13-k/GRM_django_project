from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Supply, SupplyProduct
from storage.models import Storage
from supplier.models import Supplier
from product.models import Product
from .serializers import SupplySerializer, SupplyProductSerializer, SupplyCreateSerializer


# Создание поставки с товароами
@extend_schema(
    request=SupplyCreateSerializer,
    responses={200: SupplySerializer},
    tags=['supply'],
    description="Создание поставки с товароами"
)
class SupplyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupplyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        supplier = get_object_or_404(Supplier, id=data['supplier_id'])
        storage = get_object_or_404(Storage, id=data['storage_id'])

        if storage.company != user.company:
            raise PermissionDenied("Склад не вашей компании")

        if supplier.company != user.company:
            raise PermissionDenied("Поставщик не вашей компании")

        supply = Supply.objects.create(supplier=supplier, storage=storage)

        for item in data['products']:
            product = get_object_or_404(Product, id=item['id'])

            quantity = item['quantity']

            if quantity <= 0:
                raise PermissionDenied("Количество должно быть больше 0")

            if product.storage.company != user.company:
                raise PermissionDenied("Товар не вашей компании")

            SupplyProduct.objects.create(supply=supply, product=product, quantity=quantity)

        return Response({"detail": "Поставка создана"})


# Просмотр поставки
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID поставки'
                             ),
        ],
        responses={200: SupplySerializer},
        tags=['supply'],
        description="Просмотр поставки (доступен пользователям компании)"
)
class SupplyDetailView(RetrieveAPIView):
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        supply = get_object_or_404(Supply, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")
        if supply.storage.company != user.company:
            raise PermissionDenied("Поставка не принадлежит вашей компании")

        return supply


# Список поставок
@extend_schema(
    responses={200: SupplySerializer(many=True)},
    tags=['supply'],
    description="Список всех поставок вашей компании (доступно всем сотрудникам компании)"
)
class SupplyListView(ListAPIView):
    serializer_class = SupplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        storage_id = self.request.query_params.get('storage')

        if storage_id:
            storage = get_object_or_404(Storage, id=storage_id)

            if storage.company != user.company:
                raise PermissionDenied("Вы не привязаны к компании")
            return Supply.objects.filter(storage=storage)
        return Supply.objects.filter(storage__company=user.company)


# Удаление поставки
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID поставки'
                             ),
        ],
        responses={204: None},
        tags=['supply'],
        description="Удаление поставки (только владелец компании)"
)
class SupplyDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        supply = get_object_or_404(Supply, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if supply.storage.company != user.company:
            raise PermissionDenied("Поставка не принадлежит вашей компании")

        if not user.is_company_owner:
            raise PermissionDenied("Только владелец компании может удалить поставку")

        return supply

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Поставка {instance.title} удалена"},
            status=status.HTTP_200_OK
        )
