from django.urls import path
from . import views

urlpatterns = [
    path('npv/', views.calculate_NPV_form, name='calculate-npv'),  # URL for the NPV calculation form
    path('list_evaluations/', views.list_evaluations, name='list_evaluations'),
]
