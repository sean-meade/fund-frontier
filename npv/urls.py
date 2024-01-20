from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # URL for the home page
    path('about/', views.about, name='about'),  # URL for the about page
    path('contact/', views.contact, name='contact'),  # URL for the contact page
    path('calculate-npv/', views.calculate_NPV_form, name='calculate-npv'),  # URL for the NPV calculation form
    path('list-evaluations/', views.list_evaluations, name='list-evaluations'),  # URL for listing evaluations
    path('list-evaluation-projects/<int:evaluation_id>', views.list_evaluation_projects, name='list-evaluation-projects'),  # URL for listing evaluations
]
