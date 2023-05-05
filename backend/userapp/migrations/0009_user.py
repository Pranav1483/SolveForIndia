# Generated by Django 4.2 on 2023-04-05 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0008_delete_user_remove_block_owned_block_owner_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('mobile', models.CharField(blank=True, max_length=15)),
            ],
        ),
    ]
