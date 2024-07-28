# Generated by Django 4.2.14 on 2024-07-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hp_name', models.CharField(max_length=50)),
                ('hp_address', models.CharField(max_length=100)),
                ('hp_phone', models.CharField(max_length=15, null=True)),
            ],
        ),
    ]
