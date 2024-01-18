from django.urls import path
from . import views

urlpatterns = [
    path('', views.calculate_NPV_form, name='calculate-npv'),  # URL for the NPV calculation form
    path('list-projects/', views.list_projects, name='list-projects'),
]
