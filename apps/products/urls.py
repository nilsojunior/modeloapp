from django.urls import path
from .           import views

app_name = "products"

urlpatterns = [
    path("listar/", views.list_products, name = "list_products"),
    path("adicionar/", views.add_product, name = "add_product"),
    path("editar/<int:id>/", views.edit_product, name = "edit_product"),
    path("excluir/<int:id>/", views.delete_product, name = "delete_product"),
]
