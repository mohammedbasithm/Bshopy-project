from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.
def home(request):
    categories=Category.objects.all()
    
    products=Product.objects.all()

    return render(request,'home.html',{'categories':categories,'products':products})

def men(request):
    return render(request,'men.html')

def category(request,slug):
    categories = get_object_or_404(Category, slug=slug)
    products = categories.product_set.all()  # Retrieve products based on the category
    
    return render(request,'category.html',{'products':products,'category':categories})

def productdetails(request, slug):
    print(slug)
    product_variant=ProductVariant.objects.get(slug=slug)
    # product_variant = get_object_or_404(ProductVariant, slug=slug)
    product = product_variant.product
    images = ProductImage.objects.filter(variant=product_variant)

    return render(request, 'productdetails.html', {
        'product': product,
        'product_variant': product_variant,
        'images': images,
        'selected_variant': product_variant  # Add this line
    })
from django.core.paginator import Paginator
def shop(request):  
    products = Product.objects.filter(is_active=True)
    price = ProductVariant.objects.filter(product__in=products).all()
    categories = Category.objects.all()
    brands = Brands.objects.all() 


    if request.method=='POST':
        searched=request.POST['search']
        products=Product.objects.filter(name__icontains=searched)
    if request.method == "GET":
        # Handling filters from the request
        category_filter = request.GET.get('categoryFilter')
        brand_filter = request.GET.get('brandFilter')
        price_filter = request.GET.get('priceFilter')

        # Apply the filters to the products queryset based on the criteria
        if category_filter and category_filter != 'all':
            products = products.filter(category=category_filter)

        if brand_filter and brand_filter != 'all':
            products = products.filter(brand_name=brand_filter)

         # Apply other filters based on the 'price_filter' value as needed
        if price_filter == 'under50':
            products = products.filter(productvariant__price__lt=5000)
        elif price_filter == '50to100':
            products = products.filter(productvariant__price__range=(5000, 30000))
        elif price_filter == '100to200':
            products = products.filter(productvariant__price__range=(30000, 50000))
        #Add more price range options as needed

    paginator = Paginator(products, 9)  # Display 9 categories per page
    page_number = request.GET.get('page')
    products_paginator = paginator.get_page(page_number)
    context = {
        "products": products_paginator,
        "price": price,  # Add price to the context for the template
        'categories': categories,
        'brands': brands,
    }

    return render(request, 'shop.html', context)

def get_variant(request):
    if request.method == 'GET':
        print("REACHED Get Variant")
        product_id = request.GET.get('product_id')
        product_obj=Product.objects.get(id=product_id)
        product_variant=ProductVariant.objects.filter(product=product_obj)
        print("REACHED Get Variant-------------")
        variant_list = []
        for variant in product_variant:
            variant_dict = {
                "id": variant.id,
                "size": variant.size.size,
            # Add other fields as needed
            }
            variant_list.append(variant_dict)

        # Serialize the list of dictionaries to JSON
        response_data = {"variants": variant_list}
        # response_data = product_variant
        return JsonResponse(response_data)
    
