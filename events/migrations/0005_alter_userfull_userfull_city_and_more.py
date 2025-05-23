# Generated by Django 5.1.6 on 2025-03-04 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfull',
            name='userFull_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_image',
            field=models.ImageField(blank=True, default='user_photos/default.png', null=True, upload_to='user_photos/'),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='userfull',
            name='userFull_zipcode',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
