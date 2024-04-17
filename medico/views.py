from django.shortcuts import render, redirect
from .models import Especialidades, DadosMedico
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
import re


def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()


# Create your views here.
def cadastro_medico(request):

    if not request.user.is_authenticated:
        messages.add_message(
            request,
            constants.WARNING,
            "Você precisa estar logado para acessar essa página.",
        )
        return redirect(reverse("login"))

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(
            request, "cadastro_medico.html", {"especialidades": especialidades}
        )

    if request.method == "POST":
        if is_medico(request.user):
            messages.add_message(
                request, constants.WARNING, "Você já está cadastrado como médico."
            )
            return redirect(
                "/medicos/abrir_horario"
            )  # TODO redirect(reverse("abrir_horario"))

        try:
            crm = request.POST["crm"]
            nome = request.POST["nome"]
            cep = request.POST.get("cep")
            rua = request.POST.get("rua")
            bairro = request.POST.get("bairro")
            numero = request.POST.get("numero")
            cim = request.FILES.get("cim")
            rg = request.FILES.get("rg")
            foto = request.FILES.get("foto")
            especialidade = request.POST.get("especialidade")
            descricao = request.POST.get("descricao")
            valor_consulta = request.POST.get("valor_consulta")

            if not crm or not nome:
                raise ValueError("Preencha todos os campos obrigatórios.")

            if valor_consulta == "" or int(valor_consulta) < 0:
                raise ValueError("Valor da consulta deve ser positivo.")

            if numero == "" or int(numero) < 0:
                raise ValueError("Número da residência deve ser positivo.")

            if not re.match(r"^[0-9]{5}-[\d]{3}$", cep):
                raise ValueError("CEP inválido. O formato correto é XXXXX-XXX.")

            dados_medico = DadosMedico(
                crm=crm,
                nome=nome,
                cep=cep,
                rua=rua,
                bairro=bairro,
                numero=numero,
                rg=rg,
                cedula_identidade_medica=cim,
                foto=foto,
                user=request.user,
                descricao=descricao,
                especialidade_id=especialidade,
                valor_consulta=valor_consulta,
            )
            dados_medico.save()

            messages.add_message(
                request, constants.SUCCESS, "Cadastro médico realizado com sucesso."
            )

            return render(
                request, "cadastro_medico.html"
            )  # TODO redirect(reverse("abrir_horario")
        except Exception as e:
            messages.add_message(
                request, constants.ERROR, f"Erro ao cadastrar médico. {e}"
            )
            return redirect(reverse("cadastro_medico"))
