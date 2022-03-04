# Generated by Django 3.2.12 on 2022-03-03 18:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_requests_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='color',
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('color', models.CharField(max_length=7)),
                ('quantity', models.IntegerField(default=0)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='cars.car', verbose_name='cars')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]