from django.urls import path
from .           import views

app_name = "clients"

urlpatterns = [
    path("listar/", views.list_clients, name = "list_clients"),
    path("adicionar/", views.add_client, name = "add_client"),
    path("editar/<int:id>/", views.edit_client, name = "edit_client"),
    path("excluir/<int:id>/", views.delete_client, name = "delete_client"),
]
