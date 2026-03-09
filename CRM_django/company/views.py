from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, NotFound
from .serializers import CompanySerializer, AddEmployeeSerializer
from .models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

@extend_schema(
        request=CompanySerializer,
        responses={201: CompanySerializer},
        tags=['company'],
        description="Создание компании"
)

class CompanyView(CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.company is not None:
            raise PermissionDenied("У вас уже есть компания")

        company = serializer.save(owner=self.request.user)

        self.request.user.company = company
        self.request.user.is_company_owner = True
        self.request.user.save()

class CompanyEmployeeAddView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=AddEmployeeSerializer,
        responses={200: None},
        tags=['company'],
        description="Добавление пользователя в компанию (только владелец компании)"
    )

    def post(self, request):
        if not request.user.is_company_owner or not request.user.company:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        serializer = AddEmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        user = None

        if 'user_id' in data:
            try:
                user = User.objects.get(id=data['user_id'])
            except User.DoesNotExist:
                raise NotFound('Пользователь с таким id не найден')
        elif 'email' in data:
            try:
                user = User.objects.get(email=data['email'])
            except User.DoesNotExist:
                raise NotFound('Пользователь с таким email не найден')

        if user.is_company_owner:
            raise PermissionDenied("Нельзя добавить владельца другой компании")

        if user.company:
            raise PermissionDenied("Пользователь уже состоит в компании")

        user.company = request.user.company
        user.save()

        return Response(
            {"detail": f"Пользователь {user.username} добавлен в компанию"},
            status=status.HTTP_200_OK
        )


@extend_schema(
    responses={200: None},
    tags=['company'],
    description="Просмотр компании. Доступно только владельцу компании."
)
class CompanyDetailView(RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
       return get_object_or_404(Company, pk=self.kwargs['pk'])


@extend_schema(
        responses={200: CompanySerializer},
        tags=['company'],
        description="Обновление данных компании. Доступно только владельцу компании."
)
class CompanyUpdateView(UpdateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        user = self.request.user

        if not hasattr(user, 'company') or user.company is None:
            raise PermissionDenied("У вас нет компании")

        elif not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return user.company


@extend_schema(
        responses={204: None},
        tags=['company'],
        description="Удаление компании. Доступно только владельцу компании."
)
class CompanyDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if not hasattr(user, 'company') or user.company is None:
            raise PermissionDenied("У вас нет компании")

        elif not user.is_company_owner:
            raise PermissionDenied("Вы не являетесь владельцем компании")

        return user.company










