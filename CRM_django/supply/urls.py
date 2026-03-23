from django.urls import path
from .views import (
    SupplyCreateView,
    SupplyDetailView,
    SupplyDeleteView,
    SupplyListView,
)

urlpatterns = [
    path('create/', SupplyCreateView.as_view(), name='supply-create'),
    path('<int:pk>/', SupplyDetailView.as_view(), name='supply-detail'),
    path('<int:pk>/delete/', SupplyDeleteView.as_view(), name='supply-delete'),
    path('list/', SupplyListView.as_view(), name='supply-list'),
]