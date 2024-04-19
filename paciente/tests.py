from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import DatasAbertas, Consulta


class AgendarHorarioTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.data_aberta = DatasAbertas.objects.create(
            agendado=False, data="2021-01-01 12:00:00", user=self.user
        )
        self.url = reverse("agendar_horario", args=[self.data_aberta.id])

    def test_agendar_horario(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Consulta.objects.filter(
                paciente=self.user, data_aberta=self.data_aberta
            ).exists()
        )
        self.data_aberta.refresh_from_db()
        self.assertTrue(self.data_aberta.agendado)
