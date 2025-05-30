from django.db import models

# Create your models here.
class TrackedStock(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='stock_images/',blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.symbol} - {self.company_name}"

class Testimonial(models.Model):
    name = models.CharField(max_length=20)
    profession = models.CharField(max_length=20)
    title = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='stock_images/',blank=True)
    
    def __str__(self):
        return f"{self.name}"
