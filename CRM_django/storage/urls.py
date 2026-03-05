from django.urls import path
from .views import (
    StorageCreateView,
    StorageDetailView,
    StorageUpdateView,
    StorageDeleteView,
)

urlpatterns = [
    path('create/', StorageCreateView.as_view(), name='storage-create'),
    path('<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
    path('<int:pk>/update/', StorageUpdateView.as_view(), name='storage-update'),
    path('<int:pk>/delete/', StorageDeleteView.as_view(), name='storage-delete'),
]