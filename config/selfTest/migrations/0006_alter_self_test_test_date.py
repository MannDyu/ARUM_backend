# Generated by Django 4.2.14 on 2024-08-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfTest', '0005_alter_self_test_result_result_subheading'),
    ]

    operations = [
        migrations.AlterField(
            model_name='self_test',
            name='test_date',
            field=models.DateField(auto_now=True),
        ),
    ]
