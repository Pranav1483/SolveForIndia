# Generated by Django 4.2 on 2023-04-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='hash_code',
            field=models.CharField(max_length=100),
        ),
    ]
