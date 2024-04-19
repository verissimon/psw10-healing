from django.shortcuts import render, redirect
from django.urls import reverse
from medico.models import DadosMedico, DatasAbertas, Especialidades
from django.db import transaction
from paciente.models import Consulta
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from medico.views import is_medico


def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()
        medico_filtro = request.GET.get("medico")
        especs_filtro = request.GET.getlist("especialidades")
        consultas = Consulta.objects.filter(
            paciente=request.user, data_aberta__data__gte=datetime.now()
        )
        # print(consultas)

        if medico_filtro:
            medicos = medicos.filter(nome__icontains=medico_filtro)

        if especs_filtro:
            medicos = medicos.filter(especialidade_id__in=especs_filtro)

        return render(
            request,
            "home.html",
            {
                "medicos": medicos,
                "especialidades": especialidades,
                "consultas": consultas,
                "is_medico": is_medico(request.user),
            },
        )


def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = (
            DatasAbertas.objects.filter(user=medico.user)
            .filter(data__gte=datetime.now())
            .filter(agendado=False)
            .order_by("data")
        )
        return render(
            request,
            "escolher_horario.html",
            {
                "medico": medico,
                "datas_abertas": datas_abertas,
                "is_medico": is_medico(request.user),
            },
        )


def agendar_horario(request, id_data_aberta):
    if request.method == "GET":  # agenda horario de consulta e atualiza data_aberta
        with transaction.atomic():
            data_aberta = DatasAbertas.objects.get(id=id_data_aberta)
            horario_agendado = Consulta(paciente=request.user, data_aberta=data_aberta)
            horario_agendado.save()
            data_aberta.agendado = True
            data_aberta.save()

        messages.add_message(
            request, constants.SUCCESS, "Consulta agendada com sucesso!"
        )

        return redirect(reverse("minhas_consultas"))


def minhas_consultas(request):
    if request.method == "GET":
        minhas_consultas = Consulta.objects.filter(
            paciente=request.user,
            #data_aberta__data__gte=datetime.now()
        )

        data_filtro = request.GET.get("data")
        especs_filtro = request.GET.get("especialidades")

        if data_filtro:
            minhas_consultas = minhas_consultas.filter(
                data_aberta__data__date=data_filtro
            )

        if especs_filtro:
            medicos_agendados = DadosMedico.objects.filter(
                especialidade__especialidade__icontains=especs_filtro
            )
            minhas_consultas = minhas_consultas.filter(
                data_aberta__user_id__in=medicos_agendados.values_list(
                    "user_id", flat=True
                )
            )

        return render(
            request,
            "minhas_consultas.html",
            {
                "minhas_consultas": minhas_consultas,
                "is_medico": is_medico(request.user),
            },
        )


def consulta(request, id_consulta):
    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedico.objects.get(user=consulta.data_aberta.user)
        return render(
            request,
            "consulta.html",
            {
                "consulta": consulta,
                "dado_medico": dado_medico,
                "is_medico": is_medico(request.user),
            },
        )
