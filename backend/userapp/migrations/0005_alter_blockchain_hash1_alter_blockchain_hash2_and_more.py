# Generated by Django 4.2 on 2023-04-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_alter_block_hash_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain',
            name='hash1',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='hash2',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='hash3',
            field=models.CharField(max_length=1000),
        ),
    ]
