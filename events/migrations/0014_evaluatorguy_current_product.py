# Generated by Django 5.1.6 on 2025-03-09 04:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_evaluatorguy_currently_working'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluatorguy',
            name='current_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eval_product', to='events.product'),
        ),
    ]
