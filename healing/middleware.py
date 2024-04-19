from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_req_path = "/medicos" in request.path or "/pacientes" in request.path
        if not request.user.is_authenticated and auth_req_path:
            messages.add_message(
                request,
                constants.WARNING,
                f"Você precisa estar logado para acessar {request.path}.",
            )
            return redirect(reverse("login"))
        response = self.get_response(request)
        return response
