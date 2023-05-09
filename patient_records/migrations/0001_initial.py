# Generated by Django 4.2.1 on 2023-05-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('medical_history', models.JSONField(default=dict)),
            ],
        ),
    ]
