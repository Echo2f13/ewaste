# Generated by Django 5.1.6 on 2025-02-23 08:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='userCredits',
            fields=[
                ('userCredits_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('Credits', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'User Credits',
            },
        ),
        migrations.CreateModel(
            name='deliveryGuy',
            fields=[
                ('deliveryGuy_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('deliveryGuy_image', models.ImageField(null='True', upload_to='')),
                ('deliveryGuy_phoneNumber', models.CharField(max_length=15, unique=True)),
                ('deliveryGuy_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deliveryGuy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Delivery Guy',
            },
        ),
        migrations.CreateModel(
            name='evaluatorGuy',
            fields=[
                ('evaluatorGuy_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('evaluatorGuy_image', models.ImageField(null='True', upload_to='')),
                ('evaluatorGuy_phoneNumber', models.CharField(max_length=15, unique=True)),
                ('evaluatorGuy_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluatorGuy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Evaluator Guy',
            },
        ),
        migrations.CreateModel(
            name='userFull',
            fields=[
                ('userFull_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('userFull_image', models.ImageField(null='True', upload_to='user_photos/')),
                ('userFull_phoneNumber', models.CharField(max_length=15, unique=True)),
                ('userFull_street', models.CharField(max_length=255, null='True')),
                ('userFull_city', models.CharField(max_length=100, null='True')),
                ('userFull_state', models.CharField(max_length=100, null='True')),
                ('userFull_zipcode', models.CharField(max_length=20, null='True')),
                ('userFull_country', models.CharField(max_length=100, null='True')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userFull', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Full User',
            },
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('product_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('product_category', models.CharField(choices=[('MOB_TAB', 'Mobiles and Tablets'), ('LAP_COMP', 'Laptops and Computers'), ('TV_MON', 'Televisions and Monitors'), ('HOME_APP', 'Home Appliances'), ('COMP_ACC', 'Computer Accessories'), ('GAM_CON', 'Gaming Consoles'), ('AUD_VID', 'Audio and Video Devices'), ('NET_DEV', 'Networking Devices'), ('STO_DEV', 'Storage Devices'), ('CAM_CORD', 'Cameras and Camcorders'), ('WEAR', 'Wearables'), ('OFF_EQUIP', 'Office Equipment'), ('IND_ELEC', 'Industrial Electronics'), ('MED_DEV', 'Medical Devices'), ('MISC', 'Miscellaneous Electronics')], default='OTH', max_length=10)),
                ('product_description', models.CharField(max_length=5000)),
                ('product_image_1', models.ImageField(null='True', upload_to='product_photos/')),
                ('product_image_2', models.ImageField(null='True', upload_to='product_photos/')),
                ('product_image_3', models.ImageField(null='True', upload_to='product_photos/')),
                ('product_image_4', models.ImageField(null='True', upload_to='product_photos/')),
                ('product_bought_price', models.IntegerField(default=0, null='True')),
                ('product_bought_date', models.DateTimeField(blank='True', null='True')),
                ('product_evaluation_status', models.IntegerField(default=0, null='True')),
                ('product_evaluation_score', models.IntegerField(default=0, null='True')),
                ('product_discount', models.IntegerField(default=0)),
                ('product_sell_price', models.IntegerField(default=0)),
                ('product_sold', models.IntegerField(default=0)),
                ('product_onDelivery', models.IntegerField(default=0)),
                ('product_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.userfull')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='evaluatorJob',
            fields=[
                ('evaluatorJob_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('evaluatorJob_status', models.IntegerField(default=0)),
                ('evaluatorJob_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.product')),
                ('evaluatorJob_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.userfull')),
            ],
        ),
        migrations.CreateModel(
            name='deliveryJob',
            fields=[
                ('deliveryJob_id', models.BigAutoField(auto_created='True', primary_key=True, serialize=False)),
                ('deliveryJob_status', models.IntegerField(default=0)),
                ('deliveryJob_deliveryGuy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.deliveryguy')),
                ('deliveryJob_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.product')),
                ('deliveryJob_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_jobs_buyer', to='events.userfull')),
                ('deliveryJob_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_jobs_seller', to='events.userfull')),
            ],
        ),
    ]
