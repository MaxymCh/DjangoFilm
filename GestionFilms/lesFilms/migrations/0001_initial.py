# Generated by Django 4.2.5 on 2023-09-30 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('date_creation', models.DateField(auto_now_add=True)),
                ('realisateur', models.CharField(max_length=250)),
            ],
        ),
    ]
