from django.db import models
from django.contrib.auth.models import User

PRODUCT_CATEGORIES = [
    ('MOB_TAB', 'Mobiles and Tablets'),
    ('LAP_COMP', 'Laptops and Computers'),
    ('TV_MON', 'Televisions and Monitors'),
    ('HOME_APP', 'Home Appliances'),
    ('COMP_ACC', 'Computer Accessories'),
    ('GAM_CON', 'Gaming Consoles'),
    ('AUD_VID', 'Audio and Video Devices'),
    ('NET_DEV', 'Networking Devices'),
    ('STO_DEV', 'Storage Devices'),
    ('CAM_CORD', 'Cameras and Camcorders'),
    ('WEAR', 'Wearables'),
    ('OFF_EQUIP', 'Office Equipment'),
    ('IND_ELEC', 'Industrial Electronics'),
    ('MED_DEV', 'Medical Devices'),
    ('MISC', 'Miscellaneous Electronics'),
]

class userFull(models.Model):
    userFull_id = models.BigAutoField(primary_key='True', auto_created='True')
    userFull_image = models.ImageField(null='True', upload_to='user_photos/')
    userFull_phoneNumber = models.CharField(max_length=15, unique=True, null=False)
    
    # Address Fields
    userFull_street = models.CharField(max_length=255, null='True')
    userFull_city = models.CharField(max_length=100, null='True')
    userFull_state = models.CharField(max_length=100, null='True')
    userFull_zipcode = models.CharField(max_length=20, null='True')
    userFull_country = models.CharField(max_length=100, null='True')
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userFull')

    class Meta:
        db_table = 'Full User'

    def _str_(self):
        return self.user.username

class product(models.Model):
    product_id = models.BigAutoField(primary_key='True', auto_created='True')
    product_seller = models.ForeignKey(userFull, on_delete=models.CASCADE)
    
    product_category = models.CharField(max_length=10, choices=PRODUCT_CATEGORIES, default='OTH')
    product_description = models.CharField(max_length=5000)
    
    product_image_1 = models.ImageField(null='True', upload_to='product_photos/')
    product_image_2 = models.ImageField(null='True', upload_to='product_photos/')
    product_image_3 = models.ImageField(null='True', upload_to='product_photos/')
    product_image_4 = models.ImageField(null='True', upload_to='product_photos/')
    
    product_bought_price = models.IntegerField(null='True', default=0)
    product_bought_date = models.DateTimeField(null='True', blank='True')
    product_bought_date = models.DateTimeField(null='True', blank='True')
    
    product_evaluation_status = models.IntegerField(null='True', default=0)
    product_evaluation_score = models.IntegerField(null='True', default=0)
    
    product_discount = models.IntegerField(default=0)
    product_sell_price = models.IntegerField(default=0)
    
    product_sold = models.IntegerField(default=0)
    product_onDelivery = models.IntegerField(default=0)
    class Meta:
        db_table = 'Product'
    
class deliveryGuy(models.Model):
    deliveryGuy_id = models.BigAutoField(primary_key='True', auto_created='True')
    deliveryGuy_image = models.ImageField(null='True', upload_to='')
    deliveryGuy_phoneNumber = models.CharField(max_length=15, unique=True, null=False)
    
    deliveryGuy_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deliveryGuy')

    class Meta:
        db_table = 'Delivery Guy'
        
class evaluatorGuy(models.Model):
    evaluatorGuy_id = models.BigAutoField(primary_key='True', auto_created='True')
    evaluatorGuy_image = models.ImageField(null='True', upload_to='')
    evaluatorGuy_phoneNumber = models.CharField(max_length=15, unique=True, null=False)
    
    evaluatorGuy_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluatorGuy')

    class Meta:
        db_table = 'Evaluator Guy'

class userCredits(models.Model):
    userCredits_id = models.BigAutoField(primary_key='True', auto_created='True')
    Credits = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'User Credits'
    
class deliveryJob(models.Model):
    deliveryJob_id = models.BigAutoField(primary_key='True', auto_created='True')
    deliveryJob_product = models.ForeignKey(product, on_delete=models.CASCADE)
    deliveryJob_seller = models.ForeignKey(userFull, on_delete=models.CASCADE)
    deliveryJob_buyer = models.ForeignKey(userFull, on_delete=models.CASCADE)
    deliveryJob_deliveryGuy = models.ForeignKey(deliveryGuy, on_delete=models.CASCADE)
    deliveryJob_status = models.IntegerField(default=0)
    
class evaluatorJob(models.Model):
    evaluatorJob_id = models.BigAutoField(primary_key='True', auto_created='True')
    evaluatorJob_product = models.ForeignKey(product, on_delete=models.CASCADE)
    evaluatorJob_seller = models.ForeignKey(userFull, on_delete=models.CASCADE)
    evaluatorJob_status = models.IntegerField(default=0)