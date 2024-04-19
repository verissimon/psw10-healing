# Generated by Django 5.0.4 on 2024-04-18 22:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medico', '0003_datasabertas'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('A', 'Agendado'), ('C', 'Cancelada'), ('F', 'Finalizada'), ('I', 'Iniciada')], default='A', max_length=1)),
                ('link', models.URLField(blank=True, null=True)),
                ('data_aberta', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='medico.datasabertas')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='paciente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
