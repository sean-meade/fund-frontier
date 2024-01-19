from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_NPV_form, name='calculate-npv'),  # URL for the NPV calculation form
    path('list-evaluations/', views.list_evaluations, name='list-evaluations'),
]
