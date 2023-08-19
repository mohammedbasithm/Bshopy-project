from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Category)
admin.site.register(Brands)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Size)
admin.site.register(ProductImage)

