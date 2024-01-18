from . import views
from django.urls import path

urlpatterns = [
    path('', views.calculate_NPV_form, name='calculate-npv'),
]
