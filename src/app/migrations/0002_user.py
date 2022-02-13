# Generated by Django 4.0.2 on 2022-02-13 18:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('external_identifier', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=32)),
                ('fullname', models.CharField(max_length=30)),
                ('phoneNumber', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?\\d?\\d{8,15}$')])),
            ],
        ),
    ]