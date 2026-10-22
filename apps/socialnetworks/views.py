from django.shortcuts import render, get_object_or_404, redirect
from .forms           import SocialnetworkForm
from .models          import Socialnetwork

# Create your views here.

def add_socialnetwork(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = SocialnetworkForm(request.POST)
        if form.is_valid():
            f = form.save(commit = False)
            f.save()
            form.save_m2m()
            return redirect("socialnetworks:list_socialnetworks")

    template_name = "socialnetworks/add_socialnetwork.html"
    form          = SocialnetworkForm()
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def list_socialnetworks(request: HttpRequest) -> HttpResponse:
    template_name = "socialnetworks/list_socialnetworks.html"
    socialnetworks = Socialnetwork.objects.filter()
    context = {
        "socialnetworks": socialnetworks
    }
    return render(request, template_name, context)

def edit_socialnetwork(request: HttpRequest, id: int) -> HttpResponse:
    socialnetwork = get_object_or_404(Socialnetwork, id = id)
    if request.method == "POST":
        form = SocialnetworkForm(request.POST, instance = socialnetwork)
        if form.is_valid():
            form.save()
            return redirect("socialnetworks:list_socialnetworks")

    template_name = "socialnetworks/add_socialnetwork.html"
    form          = SocialnetworkForm(instance = socialnetwork)
    context       = {
        "form": form
    }
    return render(request, template_name, context)

def delete_socialnetwork(request: HttpRequest, id: int) -> HttpReponse:
    socialnetwork = Socialnetwork.objects.get(id = id)
    socialnetwork.delete()
    return redirect("socialnetworks:list_socialnetworks")
