from django.urls import path
from .views import (
    CompanyView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyEmployeeAddView,
)

urlpatterns = [
    path('create/', CompanyView.as_view(), name='company-create'),
    path('company/<int:pk>/', CompanyDetailView.as_view()),
    path('me/update/', CompanyUpdateView.as_view(), name='company-update'),
    path('me/delete/', CompanyDeleteView.as_view(), name='company-delete'),
    path('employees/', CompanyEmployeeAddView.as_view(), name='company-add-employee'),
]