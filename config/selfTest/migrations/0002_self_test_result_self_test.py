# Generated by Django 4.2.14 on 2024-08-02 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('selfTest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Self_test_result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_score', models.IntegerField()),
                ('max_score', models.IntegerField()),
                ('result_subheading', models.CharField(max_length=15)),
                ('result_content', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Self_test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.IntegerField()),
                ('test_date', models.DateField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
