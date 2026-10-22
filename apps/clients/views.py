from django.shortcuts import render, get_object_or_404, redirect
from .forms           import ClientForm
from .models          import Client, Socialnetwork

# Create your views here.

def add_client(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.save()
            form.save_m2m()
            return redirect("clients:list_clients")

    template_name = "clients/add_client.html"
    form          = ClientForm()
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def list_clients(request: HttpRequest) -> HttpResponse:
    template_name = "clients/list_clients.html"
    clients       = Client.objects.prefetch_related("socialnetwork")
    context = {
        "clients" : clients,
    }
    return render(request, template_name, context)

def edit_client(request: HttpRequest, id: int) -> HttpResponse:
    client = get_object_or_404(Client, id = id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance = client)
        if form.is_valid():
            form.save()
            return redirect("clients:list_clients")

    template_name = "clients/add_client.html"
    form          = ClientForm(instance = client)
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def delete_client(request: HttpRequest, id: int) -> HttpResponse:
    client = Client.objects.get(id = id)
    client.delete()
    return redirect("clients:list_clients")
