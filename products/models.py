from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class Product(models.Model):
    name = models.CharField(max_length=100)
    barcode = models.ImageField(upload_to='barcode_images/', blank=True)
    country_id = models.CharField(max_length=1, null=True)
    manufacturer_id = models.CharField(max_length=6, null=True)
    product_id = models.CharField(max_length=5, null=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        EAN = barcode.get_barcode_class('ean13')
        ean = EAN(f'{self.country_id}{self.manufacturer_id}{self.product_id}', writer = ImageWriter())
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save(f'barcode{self.id}.png', File(buffer), save=False)
        return super().save(*args, **kwargs)