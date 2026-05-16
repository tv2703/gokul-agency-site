# ads/models.py
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('school', 'School Stationery'),
        ('office', 'Office Stationery'),
    ]

    title = models.CharField(max_length=150, verbose_name="Product Name")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='school')
    short_description = models.CharField(max_length=255, help_text="Displayed directly in the gallery grid")
    detailed_description = models.TextField(help_text="Displayed inside the popup modal")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

# New Model to store up to 10 images per product
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/', help_text="Product gallery image")

    def __str__(self):
        return f"Image for {self.product.title}"