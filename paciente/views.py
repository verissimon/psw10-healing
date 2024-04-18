from django.shortcuts import render
from medico.models import DadosMedico, DatasAbertas, Especialidades
from datetime import datetime

def home(request):
    if request.method == "GET":
        medicos = DadosMedico.objects.all()
        especialidades = Especialidades.objects.all()
        medico_filtro = request.GET.get("medico")
        especs_filtro = request.GET.getlist("especialidades")
        # TODO Lembrete

        if medico_filtro:
            medicos = medicos.filter(nome__icontains=medico_filtro)

        if especs_filtro:
            medicos = medicos.filter(especialidade_id__in=especs_filtro)

        return render(
            request, "home.html", {"medicos": medicos, "especialidades": especialidades}
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
            {"medico": medico, "datas_abertas": datas_abertas},
        )
