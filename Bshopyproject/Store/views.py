from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import *
from banner.models import Banner

# Create your views here.
def home(request):
    categories=Category.objects.all()
    banner=Banner.objects.all()
    products=Product.objects.all()[:8]
    context={
        'categories':categories,
        'products':products,
        'banners':banner,
        }
    return render(request,'home.html',context)

def category(request,slug):
    categories = get_object_or_404(Category, slug=slug)
    products = categories.product_set.all()  # Retrieve products based on the category
    
    return render(request,'category.html',{'products':products,'category':categories})

def productdetails(request, slug):
    product_variant = get_object_or_404(ProductVariant, slug=slug)
    product = product_variant.product
    images = ProductImage.objects.filter(variant=product_variant)
    
    # Fetch related products using the same category and excluding the current product
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(slug=product.slug)[:4]
        
    return render(request, 'productdetails.html', {
        'product': product,
        'product_variant': product_variant,
        'images': images,
        'selected_variant': product_variant,  # Add this line
        'related_products': related_products
    })
from django.core.paginator import Paginator
def shop(request):  
    products = Product.objects.filter(is_active=True)
    price = ProductVariant.objects.filter(product__in=products).all()
    categories = Category.objects.all()
    brands = Brands.objects.all() 
    if request.method=='GET':
        sort_option = request.GET.get('sort', 'latest')
        if sort_option == 'latest':
            products= Product.objects.all().order_by('-id')
        elif sort_option == 'A-Z':
            products = Product.objects.all().order_by('name')
        elif sort_option == 'bestoffer':
            products = Product.objects.filter(productvariant__discount__isnull=False).order_by('-productvariant__discount')
    searched=None
    count=0
    if request.method=='POST':
        searched=request.POST['search']
        products=Product.objects.filter(name__icontains=searched)
        count=products.count()
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
        if price_filter == 'under 5000':
            products = products.filter(productvariant__price__lt=5000)
        elif price_filter == '5000 to 10000':
            products = products.filter(productvariant__price__range=(5000, 10000))
        elif price_filter == '10000 to 20000':
            products = products.filter(productvariant__price__range=(10000, 20000))
        #Add more price range options as needed

    paginator = Paginator(products, 7)  # Display 9 categories per page
    page_number = request.GET.get('page')
    products_paginator = paginator.get_page(page_number)
    context = {
        "products": products_paginator,
        "price": price,  # Add price to the context for the template
        'categories': categories,
        'brands': brands,
        'search':searched,
        'count':count,
    }

    return render(request, 'shop.html', context)


def get_variant(request):
    if request.method == 'GET':
        
        product_id = request.GET.get('product_id')
        product_obj=Product.objects.get(id=product_id)
        product_variant=ProductVariant.objects.filter(product=product_obj)
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
    
