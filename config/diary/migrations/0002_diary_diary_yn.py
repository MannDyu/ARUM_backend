# Generated by Django 5.0.7 on 2024-07-30 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diary',
            name='diary_yn',
            field=models.BooleanField(default=False),
        ),
    ]
