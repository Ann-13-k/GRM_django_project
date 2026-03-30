from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Sale, ProductSale
from product.models import Product
from .serializers import SaleSerializer, SaleCreateSerializer, SaleUpdateSerializer


# Создание продажи
@extend_schema(
    request=SaleCreateSerializer,
    responses={200: SaleSerializer},
    tags=['sale'],
    description="Создание продажи"
)
class SaleCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SaleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = request.user

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        sale = Sale.objects.create(buyer_name=data['buyer_name'], company=user.company)

        for item in data['product_sales']:
            product = get_object_or_404(Product, id=item['product'])

            quantity = item['quantity']

            if quantity <= 0:
                raise PermissionDenied("Количество должно быть больше 0")

            if product.quantity < quantity:
                raise PermissionDenied("Недостаточно товара на складе")

            if product.storage.company != user.company:
                raise PermissionDenied("Товар не принадлежит вашей компании")

            ProductSale.objects.create(sale=sale, product=product, quantity=quantity)

        return Response({"detail": "Продажа успешно создана"}, status=status.HTTP_200_OK)


# Просмотр продажи
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продажи'
                             ),
        ],
        responses={200: SaleSerializer},
        tags=['sale'],
        description="Просмотр продажи (доступен пользователям компании)"
)
class SaleDetailView(RetrieveAPIView):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        sale = get_object_or_404(Sale, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")
        if sale.company != user.company:
            raise PermissionDenied("Продажа не принадлежит вашей компании")

        return sale


# Список продаж
@extend_schema(
    responses={200: SaleSerializer(many=True)},
    tags=['sale'],
    description="Список всех продаж вашей компании (доступно всем сотрудникам компании)"
)
class SaleListView(ListAPIView):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.company:
            raise PermissionDenied("Вы не привязаны к компании")

        queryset = Sale.objects.filter(company=user.company)

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            queryset = queryset.filter(sale_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(sale_date__lte=end_date)

        return queryset


# Обновление продажи
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продажи'
                             ),
        ],
        responses={200: SaleSerializer},
        tags=['sale'],
        description="Обновление продажи (доступен пользователям компании)"
)
class SaleUpdateView(UpdateAPIView):
    serializer_class = SaleUpdateSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user
        sale = get_object_or_404(Sale, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if sale.company != user.company:
            raise PermissionDenied("Продажа не принадлежит вашей компании")

        return sale


# Удаление продажи
@extend_schema(
        parameters=[
            OpenApiParameter(name='pk',
                             type=OpenApiTypes.INT,
                             location=OpenApiParameter.PATH,
                             description='ID продажи'
                             ),
        ],
        responses={204: None},
        tags=['sale'],
        description="Удаление продажи"
)
class SaleDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        sale = get_object_or_404(Sale, pk=self.kwargs['pk'])

        if not user.company:
            raise PermissionDenied("Вы не привязаны к данной компании")

        if sale.company != user.company:
            raise PermissionDenied("Продажа не принадлежит вашей компании")

        return sale

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        for item in instance.product_sales.all():
            product = item.product
            product.quantity += item.quantity
            product.save()

        self.perform_destroy(instance)

        return Response(
            {"detail": f"Продажа на имя {instance.buyer_name} от {instance.sale_date} удалена"},
            status=status.HTTP_200_OK
        )
