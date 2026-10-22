from django.shortcuts import render, get_object_or_404, redirect
from .forms           import ProductForm
from .models          import Product

# Create your views here.

def add_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit = False)
            f.save()
            form.save_m2m()
            return redirect("products:list_products")

    template_name = "products/add_product.html"
    form          = ProductForm()
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def list_products(request: HttpRequest) -> HttpResponse:
    template_name = "products/list_products.html"
    products      = Product.objects.filter()
    context       = {
        "products" : products
    }
    return render(request, template_name, context)

def edit_product(request: HttpRequest, id: int) -> HttpResponse:
    product = get_object_or_404(Product, id = id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance = product)
        if form.is_valid():
            form.save()
            return redirect("products:list_products")

    template_name = "products/add_product.html"
    form          = ProductForm(instance = product)
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def delete_product(request: HttpRequest, id) -> HttpResponse:
    product = Product.objects.get(id = id)
    product.delete()
    return redirect("products:list_products")
