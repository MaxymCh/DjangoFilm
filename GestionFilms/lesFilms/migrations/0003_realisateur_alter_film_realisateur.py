# Generated by Django 4.2.5 on 2023-10-01 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lesFilms', '0002_alter_film_date_creation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Realisateur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250)),
                ('prenom', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='film',
            name='realisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='films', to='lesFilms.realisateur'),
        ),
    ]