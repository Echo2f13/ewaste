# Generated by Django 5.1.6 on 2025-03-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_deliveryguy_currently_working'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluatorguy',
            name='currently_working',
            field=models.IntegerField(default=0),
        ),
    ]
