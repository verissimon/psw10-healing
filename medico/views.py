from django.shortcuts import render, redirect
from .models import Especialidades, DadosMedico, DatasAbertas
from paciente.models import Consulta
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from datetime import datetime, timedelta
import re


def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()


# Create your views here.
def cadastro_medico(request):

    if is_medico(request.user):
        messages.add_message(
            request, constants.WARNING, "Você já está cadastrado como médico."
        )
        return redirect(reverse("abrir_horario"))

    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(
            request,
            "cadastro_medico.html",
            {"especialidades": especialidades, "is_medico": is_medico(request.user)},
        )

    if request.method == "POST":
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

            return redirect(reverse("abrir_horario"))
        except Exception as e:
            messages.add_message(
                request, constants.ERROR, f"Erro ao cadastrar médico. {e}"
            )
            return redirect(reverse("cadastro_medico"))


def abrir_horario(request):

    if not is_medico(request.user):
        messages.add_message(
            request, constants.WARNING, "Você não é um médico cadastrado."
        )
        return redirect(reverse("cadastro_medico"))

    if request.method == "GET":
        dados_medicos = DadosMedico.objects.get(user=request.user)
        datas_abertas = DatasAbertas.objects.filter(user=request.user).order_by("data")
        return render(
            request,
            "abrir_horario.html",
            {
                "dados_medicos": dados_medicos,
                "datas_abertas": datas_abertas,
                "is_medico": is_medico(request.user),
            },
        )

    if request.method == "POST":
        data = request.POST.get("data")
        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")

        if data_formatada <= datetime.now():
            messages.add_message(
                request, constants.WARNING, "Data inválida. Deve ser uma data futura."
            )
            return redirect(reverse("abrir_horario"))

        horario_abrir = DatasAbertas(data=data, user=request.user)
        horario_abrir.save()

        messages.add_message(
            request, constants.SUCCESS, "Horário cadastrado com sucesso."
        )
        return redirect(reverse("abrir_horario"))


def consultas_medico(request):
    if not is_medico(request.user):
        messages.add_message(
            request, constants.WARNING, "Somente médicos podem acessar essa página."
        )
        return redirect(reverse("logout"))

    if request.method == "GET":
        data_filter = request.GET.get("data")
        hoje = datetime.now().date()
        consultas_all = Consulta.objects.filter(data_aberta__user=request.user)

        if data_filter:
            data_filter = datetime.strptime(data_filter, "%Y-%m-%d")
            consultas_all = consultas_all.filter(data_aberta__data__date=data_filter)
            print(consultas_all.values("id"))

        consultas_hoje = consultas_all.filter(data_aberta__data__gte=hoje).filter(
            data_aberta__data__lt=hoje + timedelta(days=1)
        )

        consultas_restantes = consultas_all.exclude(id__in=consultas_hoje.values("id"))

        return render(
            request,
            "consultas_medico.html",
            {
                "consultas_hoje": consultas_hoje,
                "consultas_restantes": consultas_restantes,
                "is_medico": is_medico(request.user),
            },
        )


def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(
            request, constants.WARNING, "Somente médicos podem acessar essa página."
        )
        return redirect(reverse("logout"))

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        return render(
            request,
            "consulta_area_medico.html",
            {"consulta": consulta, "is_medico": is_medico(request.user)},
        )

    if request.method == "POST":
        try:
            consulta = Consulta.objects.get(id=id_consulta)
            link = request.POST.get("link")

            if not link:
                raise ValueError("Informe o link da consulta.")

            if consulta.status == "C":
                messages.add_message(
                    request, constants.WARNING, "Consulta já foi cancelada."
                )
                return redirect(reverse("consulta_area_medico", args=[consulta.id]))
            elif consulta.status == "F":
                messages.add_message(
                    request, constants.WARNING, "Consulta já foi finalizada."
                )
                return redirect(reverse("consulta_area_medico", args=[consulta.id]))

            consulta.link = link
            consulta.status = "I"
            consulta.save()
            messages.add_message(
                request, constants.SUCCESS, "Consulta atualizada com sucesso."
            )
            return redirect(reverse("consultas_medico"))
        except Exception as e:
            messages.add_message(
                request, constants.ERROR, f"Erro ao atualizar consulta. {e}"
            )
            return redirect(reverse("consulta_area_medico", args=[consulta.id]))


def finalizar_consulta(request, id_consulta):
    if not is_medico(request.user):
        messages.add_message(
            request, constants.WARNING, "Somente médicos podem acessar essa página."
        )
        return redirect(reverse("logout"))
    consulta = Consulta.objects.get(id=id_consulta)

    if consulta.data_aberta.user != request.user:
        messages.add_message(
            request,
            constants.WARNING,
            "Você não tem permissão para finalizar essa consulta.",
        )
        return redirect(reverse("consultas_medico"))
    
    if consulta.status == "F":
        messages.add_message(
            request,
            constants.WARNING,
            "Consulta já foi finalizada.",
        )
        return redirect(reverse("consulta_area_medico", args=[consulta.id]))

    consulta.status = "F"
    consulta.save()
    messages.add_message(
        request,
        constants.SUCCESS,
        f"Consulta de {consulta.data_aberta} com paciente {consulta.paciente} finalizada com sucesso.",
    )
    return redirect(reverse("consulta_area_medico", args=[consulta.id]))
