# Generated by Django 3.2.5 on 2024-04-13 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppm', '0003_alter_protein_organism_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='disease',
            name='protein_id',
            field=models.CharField(default='-', max_length=50, verbose_name='uniport id'),
        ),
    ]