from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),  # URL for the home page
    path('contact/', views.contact, name='contact'),  # URL for the contact page
    path('create_evaluation/', views.create_evaluation, name='create_evaluation'),  # URL for the NPV calculation form
    path('edit_evaluation/<str:evaluation_id>/', views.edit_evaluation, name='edit_evaluation'),
    path('delete_evaluation/<str:evaluation_id>/', views.delete_evaluation, name='delete_evaluation'),
    path('add_project/<int:evaluation_id>/', views.add_project, name='add_project'),  # URL for the NPV calculation form
    path('delete_project/<int:evaluation_id>/<int:project_id>/', views.delete_project, name='delete_project'),  # URL for the NPV calculation form
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),  # URL for the NPV calculation form
    path('list-evaluations/', views.list_evaluations, name='list-evaluations'),  # URL for listing evaluations
    path('list-evaluation-projects/<int:evaluation_id>/', views.list_evaluation_projects, name='list-evaluation-projects'),  # URL for listing evaluations
]
