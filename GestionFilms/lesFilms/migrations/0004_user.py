# Generated by Django 4.2.5 on 2023-10-03 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesFilms', '0003_realisateur_alter_film_realisateur'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
    ]
