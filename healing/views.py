from django.shortcuts import redirect
from django.urls import reverse

def root(request):
    return redirect(reverse("login"))


