from django.urls import path
from .views import (
    SaleCreateView,
    SaleDetailView,
    SaleListView,
    SaleUpdateView,
    SaleDeleteView,
)

urlpatterns = [
    path('create/', SaleCreateView.as_view(), name='sale-create'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<int:pk>/update/', SaleUpdateView.as_view(), name='sale-update'),
    path('<int:pk>/delete/', SaleDeleteView.as_view(), name='sale-delete'),
    path('list/', SaleListView.as_view(), name='sale-list'),
]