from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
# Create your models here.

class Category(models.Model):
    name=models.CharField( max_length=100)
    image=models.ImageField(upload_to='category')
    is_active=models.BooleanField(default=True,null=True)
    slug=models.SlugField(max_length=250,unique=True,blank=True)

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args,**kwargs)

class Brands(models.Model):
    name=models.CharField( max_length=100)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    slug=models.SlugField(blank=True)
    is_active=models.BooleanField(default=True)
    brand_name=models.ForeignKey(Brands,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        # Add the unique_together option to enforce uniqueness of product name within each brand
        unique_together = ('name', 'brand_name')

class Size(models.Model):
    size=models.CharField(max_length=10)

    def __str__(self):
        return self.size
    
class ProductVariant(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    discount_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    discount=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    stock=models.PositiveIntegerField(default=0)
    slug=models.SlugField(blank=True,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name}-{self.size}"


    def save(self, *args, **kwargs):
        self.full_clean()  # Validate the model before saving
        if not self.slug:
            slug_str = f"{self.product.name}-{self.size}"
            self.slug = slugify(slug_str)
        super().save(*args, **kwargs)
        
    
    
    
class ProductImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return f"{self.variant}-{self.image}"
    