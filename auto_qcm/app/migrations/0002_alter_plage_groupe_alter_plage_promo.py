# Generated by Django 5.1.1 on 2024-09-27 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plage',
            name='groupe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plagesgroup', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='plage',
            name='promo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plagespromo', to='auth.group'),
        ),
    ]