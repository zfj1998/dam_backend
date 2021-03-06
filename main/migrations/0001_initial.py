# Generated by Django 3.2.7 on 2021-09-03 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Msections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Mvalue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('m_time', models.DateTimeField()),
                ('m_point', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.mpoint')),
            ],
        ),
        migrations.AddField(
            model_name='mpoint',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.msections'),
        ),
    ]
