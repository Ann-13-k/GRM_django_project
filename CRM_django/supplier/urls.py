from django.urls import path
from .views import (
    SupplierCreateView,
    SupplierDetailView,
    SupplierUpdateView,
    SupplierDeleteView,
    SupplierListView,
)

urlpatterns = [
    path('create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
    path('list/', SupplierListView.as_view(), name='supplier-list'),
]