# Generated by Django 5.1.1 on 2024-09-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_reponseqcm_utilisateur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='melange_rep',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='note',
            field=models.IntegerField(default=1),
        ),
    ]