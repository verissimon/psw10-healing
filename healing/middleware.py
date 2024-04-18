from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and "/medicos" in request.path:
            messages.add_message(
                request,
                constants.WARNING,
                f"Você precisa estar logado para acessar {request.path}.",
            )
            return redirect(reverse("login"))
        response = self.get_response(request)
        return response
