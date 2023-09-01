from os import truncate
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.models import User
from Store.models import *
from django.middleware.csrf import CsrfViewMiddleware
from order.models import*
from cart.models import *
from django.contrib import messages
from django.db.models import Sum,Q
from django.db.models.functions import TruncDate
from django.utils.timezone import now
from userprofile.models import Wallet,WalletTransaction
from banner.models import Banner
from  django.views.decorators.cache import cache_control
# Create your views here.
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def adminhome(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            if not start_date and not end_date:
                # Calculate the current date
                current_date = now().date()

                # Calculate the date 30 days back from the current date
                default_start_date = current_date - timedelta(days=30)
                default_end_date = current_date

                # Convert to string format (YYYY-MM-DD)
                start_date = default_start_date.strftime('%Y-%m-%d')
                end_date = default_end_date.strftime('%Y-%m-%d')

            if start_date and end_date:
                # Corrected query filter for start_date and end_date using 'date' lookup
                order_count_date = Order.objects.filter(
                    order_date__date__gte=start_date, order_date__date__lte=end_date
                ).exclude(payment_status='CANCELLED').count()

                total_price_date = Order.objects.filter(
                    order_date__date__gte=start_date, order_date__date__lte=end_date
                ).exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

                daily_totals = Order.objects.filter(
                    order_date__date__gte=start_date, order_date__date__lte=end_date
                ).exclude(payment_status='CANCELLED').annotate(date=TruncDate('order_date')).values('date').annotate(
                    total=Sum('total_price')).order_by('date')

                order_count = Order.objects.exclude(payment_status='CANCELLED').count()
                total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']
                today = now().date()
                today_orders = Order.objects.filter(order_date__date=today)
                order_count_today = today_orders.count()
                total_price_today = sum(order.total_price for order in today_orders)  # Corrected this line

                recent_orders = Order.objects.order_by('-order_date')[:3]

                # Corrected query for top_selling_products using 'product_id' and 'product__name'
                top_selling_products = OrderItem.objects.values('product__product__name').annotate(
                    total_quantity=Sum('quantity')
                ).order_by('-total_quantity')[:5]

                categories = Category.objects.all()
                data = []

                for category in categories:
                    product_count = Product.objects.filter(category=category).count()
                    data.append(product_count)

                context = {
                    'order_count_date': order_count_date,
                    'total_price_date': total_price_date,
                    'start_date': start_date,
                    'end_date': end_date,
                    'daily_totals': daily_totals,
                    'order_count': order_count,
                    'total_price': total_price,
                    'categories': categories,
                    'data': data,
                    'order_count_today': order_count_today,
                    'total_price_today': total_price_today,
                    'recent_orders': recent_orders,
                    'top_selling_products': top_selling_products,
                }

                return render(request, 'adminside/home.html', context)

            else:
                order_count = Order.objects.exclude(payment_status='CANCELLED').count()
                total_price = Order.objects.exclude(payment_status='CANCELLED').aggregate(total=Sum('total_price'))['total']

                today = now().date()
                today_orders = Order.objects.filter(order_date__date=today)
                order_count_today = today_orders.count()
                total_price_today = sum(order.total_price for order in today_orders)  # Corrected this line

                categories = Category.objects.all()
                data = []

                for category in categories:
                    product_count = Product.objects.filter(category=category).count()
                    data.append(product_count)

                recent_orders = Order.objects.order_by('-order_date')[:3]

                # Corrected query for top_selling_products using 'product_id' and 'product__name'
                top_selling_products = OrderItem.objects.values('product__name').annotate(
                    total_quantity=Sum('quantity')
                ).order_by('-total_quantity')[:5]

                context = {
                    'order_count': order_count,
                    'total_price': total_price,
                    'start_date': start_date,
                    'end_date': end_date,
                    'order_count_today': order_count_today,
                    'total_price_today': total_price_today,
                    'categories': categories,
                    'data': data,
                    'recent_orders': recent_orders,
                    'top_selling_products': top_selling_products,
                }

                return render(request, 'adminside/home.html', context)

        return HttpResponseBadRequest("Invalid request method.")
    return redirect('signin')
from django.core.paginator import Paginator

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def user(request):
    if request.user.is_superuser:
        users=User.objects.all().order_by('id')
        context = {
            'users':users
        }

        return render(request,'adminside/user_list.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def products(request):
    if request.user.is_superuser:
        products=Product.objects.all().order_by('id')
        variants=ProductVariant.objects.filter()
        context = {
            'products':products,
        }
        return render(request,'adminside/products.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def block_user(request,user_id):
    if request.user.is_superuser:
        user=User.objects.get(id=user_id)
        user.is_active=False
        user.save()
        return redirect('user')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def unblock_user(request,user_id):
    if request.user.is_superuser:
        user=User.objects.get(id=user_id)
        user.is_active=True
        user.save()
        return redirect('user')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def delete_user(request,user_id):
    if request.user.is_superuser:
        user=User.objects.get(id=user_id)
        user.delete()
        return redirect('user')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_product(request, product_id):
    if request.user.is_superuser:
    
        products = Product.objects.get(id=product_id)
        categories = Category.objects.all()
        brands = Brands.objects.all()

        if request.method == 'POST':
            # Process form data
            products.name = request.POST['name']
            products.description = request.POST['description']
            category=request.POST['category']
            category_id=get_object_or_404(Category,id=category)
            products.category=category_id
            brand=request.POST['brand']
            brand_id=get_object_or_404(Brands,id=brand)
            products.brand_name=brand_id
            products.save()
            
            return redirect('product')

        context = {
            'products': products,
            'categories': categories,
            'brands': brands,
        }

        return render(request, 'adminside/edit_product.html', context)


    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def enable_product(request,product_id):
    if request.user.is_superuser:
        product=Product.objects.get(id=product_id)
        product.is_active=True
        product.save()
        return redirect('product')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def disable_product(request,product_id):
    if request.user.is_superuser:
        product=Product.objects.get(id=product_id)
        product.is_active=False
        product.save()
        return redirect('product')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def category(request):
    if request.user.is_superuser:
        category=Category.objects.all().order_by('id')
        context={
            'category':category
        }
        return render(request,'adminside/category.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_product(request):
    if request.user.is_superuser:
        if request.method=='POST':
            #product table
            product_name=request.POST['name']
            description=request.POST['description']
            category_name=request.POST['category']
            brand_name=request.POST['brand']
            size=request.POST['size']
            price=request.POST['price']
            stock=request.POST['stock']
            discount=request.POST['discount']
            variant_image=request.FILES.getlist('images')
            if discount:
                
                discount_price = int(price) - (int(price) * int(discount) / 100)
                discount_price=round(discount_price)
                
            else:
                discount_price=None
            #create a product
            category_id=get_object_or_404(Category,id=category_name)
            brand_id=get_object_or_404(Brands,id=brand_name)
            prod=Product.objects.create(
                name=product_name,
                description=description,
                category=category_id,
                brand_name=brand_id
                )
            #create product variant
            size_id=get_object_or_404(Size,id=size)
            product_id=get_object_or_404(Product,id=prod.id)
            new_variant=ProductVariant.objects.create(
                product=product_id,
                size=size_id,
                price=price,
                discount_price=discount_price,
                discount=int(discount),
                stock=stock,

            )

            #create product image
            
            for img in variant_image:
                new=ProductImage.objects.create(
                    variant=new_variant,
                    image=img,                       
                )
                new.save()

            return redirect('product')
        
        categories=Category.objects.all()
        sizes=Size.objects.all()
        brands=Brands.objects.all()

        context={
            'categories':categories,
            'sizes':sizes,
            'brands':brands,
        }


        return render(request,'adminside/add_product.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_category(request):
    if request.user.is_superuser:
        if request.method=='POST':
            category_name=request.POST['name']
            image=request.FILES.get('image')

            new_category=Category.objects.create(name=category_name,image=image)
            new_category.save()

            return redirect('category')
        
        return render(request,'adminside/add_category.html')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
#banner list
def banner_list(request):
    if request.user.is_superuser:
        banner=Banner.objects.all().order_by('id')
        return render(request,'adminside/banner.html',{'banners':banner})
    return redirect('signin')

#add banner
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_banner(request):
    if request.user.is_superuser:
        if request.method=='POST':
            banner_name=request.POST['banner_name']
            image=request.FILES.get('image')

            new_banner=Banner.objects.create(name=banner_name,banner_image=image)
            new_banner.save()

            return redirect('banner-list')
        
        return render(request,'adminside/add_banner.html')
    return redirect('signin')

#edit banner
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_banner(request,banner_id):
    if request.user.is_superuser:
        banner=Banner.objects.get(id=banner_id)
        if request.method=="POST":
            banner.name=request.POST['banner_name']
            banner.banner_image=request.FILES.get('image')
            banner.save()
            return redirect('banner-list')
    
        return render(request,'adminside/edit_banner.html',{'banner':banner})
    return redirect('signin')

#enable banner
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def enable_banner(request,banner_id):
    if request.user.is_superuser:
        banner=Banner.objects.get(id=banner_id)
        banner.is_active=True
        banner.save()
        return redirect('banner-list')
    return redirect('signin')

#disable banner
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def disable_banner(request,banner_id):
    if request.user.is_superuser:
        banner=Banner.objects.get(id=banner_id)
        banner.is_active=False
        banner.save()
        return redirect('banner-list')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def product_view(request,product_id):
    if request.user.is_superuser:
        product=Product.objects.get(id=product_id)
        variant=product.productvariant_set.all().order_by('id')
        context={
            'variants':variant,
            'products':product,
        }
        return render(request,'adminside/product_view.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def enable_variant(request,variant_id):
    if request.user.is_superuser:
        productvariant=ProductVariant.objects.get(id=variant_id)
        productvariant.is_active=True
        productvariant.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

def disable_variant(request,variant_id):
    if request.user.is_superuser:
        productvariant=ProductVariant.objects.get(id=variant_id)
        productvariant.is_active=False
        productvariant.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

from django.core.exceptions import ValidationError
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_variant(request, product_id):
    if request.user.is_superuser:
        product = Product.objects.get(id=product_id)
        if request.method == 'POST':
            price = request.POST['price']
            stock = request.POST['stock']
            size_id = request.POST['size']
            discount=request.POST['discount']
            variant_images = request.FILES.getlist('images')
            

            try:
                if discount:
                
                    discount_price = int(price) - (int(price) * int(discount) / 100)
                    discount_price=round(discount_price)
                
                else:
                    discount_price=None
                price = float(price)
                if price < 0:
                    messages.error(request,'Price cannot be negative.')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                    # raise ValidationError("Price cannot be negative.")

                stock = int(stock)
                if stock < 0:
                    messages.error(request,'Stock must be a non-negative integer value.')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                    # raise ValidationError("Stock must be a non-negative integer value.")

                size1 = Size.objects.get(id=size_id)
                sizess, created = Size.objects.get_or_create(size=size1)
                
                # Check if a variant with the same color already exists for the product
                existing_variant = ProductVariant.objects.filter(product=product, size=sizess).first()
                if existing_variant:
                    
                    # raise ValidationError("Size variant all ready exist.")
                    messages.error(request,'Size variant all ready exist.')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    size=size1


                new_variant = ProductVariant.objects.create(
                    product=product,
                    size=size,
                    price=price,
                    discount_price=discount_price,
                    discount=int(discount),
                    stock=stock
                )

                
                for img in variant_images:
                    ProductImage.objects.create(
                        variant=new_variant,
                        image=img
                    )

                return redirect('product')

            except (ValueError, Size.DoesNotExist, ValidationError) as e:
                error_message = str(e)
                size = Size.objects.all()
                context = {
                    'sizes': size,
                    'products': product_id,
                    'error_message': error_message,
                }
                return render(request, 'adminside/add_variant.html', context)

        size = Size.objects.all()
        context = {
            'sizes': size,
            'products': product_id,
        }
        return render(request, 'adminside/add_variant.html', context)
    return redirect('signin')

def upload_images(request):
    return render(request,'adminside/upload_images.html')


@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_variants(request,variant_id):
    if request.user.is_superuser:
        variants=ProductVariant.objects.get(id=variant_id)
        product=Product.objects.get(id=variants.product.pk)
        existing_size=variants.size.size

        if request.method=='POST':
            size_id=request.POST['size']

            size1 = Size.objects.get(id=size_id)
            if existing_size!=size1.size:
                existing_variant = ProductVariant.objects.filter(product=product, size=size1).first()
                if existing_variant:
                    
                    # raise ValidationError("Size variant all ready exist.")
                    messages.error(request,'Size variant all ready exist.')
                    return HttpResponseRedirect(request.META['HTTP_REFERER'])
                else:
                    variants.size=size1

            price=request.POST['price']
            price = float(price)
            if price < 0:
                messages.error(request,'Price cannot be negative.')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                variants.price=price
            stock=request.POST['stock']
            stock = int(stock)
            if stock < 0:
                messages.error(request,'Stock must be a non-negative integer value.')
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                variants.stock=stock

            variants.save()

            variant_images=request.FILES.getlist('images')
            if variant_images:
                
                for img in variant_images:
                    ProductImage.objects.create(
                        variant=variants,
                        image=img
                        )


            return redirect('product')
        sizes=Size.objects.all()
        images=ProductImage.objects.filter(variant=variants)
        context={
            "sizes":sizes,
            'images':images,
            'variants':variants
        }
        return render(request,'adminside/edit_variant.html',context)
    return redirect('signin')


@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def disable_category(request,category_id):
    if request.user.is_superuser:
        category=Category.objects.get(id=category_id)
        category.is_active=False
        category.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

def enable_category(request,category_id):
    if request.user.is_superuser:
        category=Category.objects.get(id=category_id)
        category.is_active=True
        category.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')


@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_category(request,category_id):
    if request.user.is_superuser:
        category=Category.objects.get(id=category_id)
        if request.method=='POST':
            category.name=request.POST['name']
            image=request.FILES.get('image')
            if image:
                category.image=image
            category.save()

            return redirect('category')
        context={
            'category':category
        }
        return render(request,'adminside/edit_category.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def order_list(request):
    if request.user.is_superuser:
        orders=Order.objects.all().order_by('-id')

        context={
            'orders':orders
        }
        return render(request,'adminside/order_list.html',context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def admin_order_view(request,order_id):
    if request.user.is_superuser:
        order_view=get_object_or_404(Order,id=order_id)
        order=OrderItem.objects.filter(order=order_view)

        context={
            'order_view':order_view,
            'orders':order
        }
        return render(request,'adminside/order_view.html',context)
    return redirect('signin')

def delete_image(request,img_id):
    if request.user.is_superuser:
        img=ProductImage.objects.get(id=img_id)
        img.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_brand(request):
    if request.user.is_superuser:
        if request.method=='POST':
            brand_name=request.POST['name']
            Brands.objects.create(name=brand_name)
        
        return render(request,'adminside/add_brand.html')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_size(request):
    if request.user.is_superuser:
        if request.method=='POST':
            size_name=request.POST['size']
            Size.objects.create(size=size_name)
        
        return render(request,'adminside/add_size.html')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def coupon_list(request):
    if request.user.is_superuser:
        coupons=Coupon.objects.all().order_by('id')

        return render(request,'adminside/coupon_list.html',{'coupons':coupons})
    return redirect('signin')

def disable_coupon(request,coupon_id):
    if request.user.is_superuser:
        coupon=Coupon.objects.get(id=coupon_id)
        coupon.is_expired=False
        coupon.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')


def enable_coupon(request,coupon_id):
    if request.user.is_superuser:

        coupon=Coupon.objects.get(id=coupon_id)
        coupon.is_expired=True
        coupon.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_coupon(request):
    if request.user.is_superuser:
        if request.method=='POST':
            coupon_code=request.POST['coupon_code']
            coupon_price=request.POST['coupon_price']
            minimum_amount=request.POST['minimum_amount']
            is_expired='is_expired' in request.POST

            Coupon.objects.create(
                coupon_code=coupon_code,
                coupon_price=coupon_price,
                minimum_amount=minimum_amount,
                is_expired=is_expired
            )
            return redirect('coupon-list')
        return render(request,'adminside/add_coupon.html')
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_coupon(request,coupon_id):
    if request.user.is_superuser:
        coupon=Coupon.objects.get(id=coupon_id)
        if request.method=='POST':
            coupon.coupon_code=request.POST['coupon_code']
            coupon.coupon_price=request.POST['coupon_price']
            coupon.minimum_amount=request.POST['minimum_amount']

            coupon.save()
            return redirect('coupon-list')
        
        return render(request,'adminside/edit_coupon.html',{'coupon':coupon})
    return redirect('signin')

def order_shipped(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        order.order_status = 'Shipped'
        print(order.order_status)
        order.shipping_date=timezone.now()
        order.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('signin')

def order_delivered(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)

        # Make sure the order is in the 'SHIPPED' status before marking it as 'DELIVERED'
        if order.order_status == 'Shipped':
            order.order_status = 'Delivered'
            print(order.order_status)
            order.delivery_date=timezone.now()
            order.return_period_expired=timezone.now()+timezone.timedelta(days=5)
            if order.payment_status=='Pending':
                order.payment_status='Paid'
            order.save()
            print(order.return_period_expired)
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('signin')

def admin_order_cancel(request, order_id):
    
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        user = order.user
        if order.order_status != 'Delivered' and order.order_status != 'Returned'and order.order_status !='Cancelled' and order.order_status != 'requested for return ':
            order_items = OrderItem.objects.filter(order=order)
            for item in order_items:
                variant = item.product
                variant.stock += item.quantity
                variant.save()
            if order.payment_method in ['razorpay', 'Wallet pay']:
                user_wallet = Wallet.objects.get(user=user)
                # Refund the amount to the user's wallet
                refund_amount = order.total_price  # Assuming you want to refund the full amount
                user_wallet.balance += Decimal(refund_amount)
                user_wallet.save()
                transaction_type = 'Cancelled'
                WalletTransaction.objects.create(
                    wallet=user_wallet,
                    amount=refund_amount,
                    order_id=order,
                    transaction_type=transaction_type,
                )
            if order.payment_status=='Pending':
                order.payment_status='No payment'
            else:
                order.payment_status='Refunded'
            order.order_status='Cancelled'
            Order.cancelled_date=timezone.now()
            order.save()

        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return redirect('signin')

def return_orders(request, order_id):
    if request.user.is_superuser:
        order = get_object_or_404(Order, id=order_id)
        user = order.user
        user_wallet, created = Wallet.objects.get_or_create(user=user)
        refund_amount = order.total_price  # Assuming you want to refund the full amount
        user_wallet.balance += Decimal(refund_amount)
        user_wallet.save()
        transaction_type='return'
        WalletTransaction.objects.create(
            wallet=user_wallet,
            amount=refund_amount,
            order_id=order,
            transaction_type=transaction_type,
            
        )
        if order.order_status != 'Cancelled':
            order.payment_status = 'Refunded'
            order.order_status = 'Returned'
            order.returned_date=timezone.now()
            order.save()

        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('signin')
    
def sales_report(request):
    if request.user.is_superuser:
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_orders = Order.objects.filter(order_date__date=today,payment_status='Paid').exclude(order_status__in=['returned', 'Cancelled'])

        order_count_today = today_orders.count()
        total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        week_orders = Order.objects.filter(order_date__range=[week_ago, today],payment_status='Paid').exclude(order_status__in=['returned', 'Cancelled'])

        order_count_week = week_orders.count()
        total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        month_orders = Order.objects.filter(order_date__range=[month_ago, today], payment_status='Paid').exclude(order_status__in=['Returned', 'Cancelled'])

        order_count_month = month_orders.count()
        total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        top_selling_variants_today = OrderItem.objects.filter(order__in=today_orders).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        top_selling_variants_week = OrderItem.objects.filter(order__in=week_orders).values(
            'product__product__name',
            'product__size__size'
        ).annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        top_selling_variants_month = OrderItem.objects.filter(order__in=month_orders).values(
            'product__product__name',
            'product__size__size'
        ).annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        context = {
            'order_count_today': order_count_today,
            'total_price_today': total_price_today,
            'order_count_week': order_count_week,
            'total_price_week': total_price_week,
            'order_count_month': order_count_month,
            'total_price_month': total_price_month,
            'top_selling_variants_today': top_selling_variants_today,
            'top_selling_variants_week': top_selling_variants_week,
            'top_selling_variants_month': top_selling_variants_month,
        }

        return render(request, 'adminside/sales_report.html', context)
    return redirect('signin')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def admin_profile(request):
    if request.user.is_superuser:
        user=request.user
        return render(request,'adminside/admin_profile.html',{'user':user})
    return redirect('signin')

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
def generate_pdf(request):
    if request.user.is_superuser:
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        today_orders = Order.objects.filter(order_date__date=today,payment_status='Paid').exclude(order_status__in=['returned', 'Cancelled'])

        order_count_today = today_orders.count()
        total_price_today = today_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        week_orders = Order.objects.filter(order_date__range=[week_ago, today],payment_status='Paid').exclude(order_status__in=['returned', 'Cancelled'])

        order_count_week = week_orders.count()
        total_price_week = week_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        month_orders = Order.objects.filter(order_date__range=[month_ago, today], payment_status='Paid').exclude(order_status__in=['Returned', 'Cancelled'])

        order_count_month = month_orders.count()
        total_price_month = month_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        top_selling_variants_today = OrderItem.objects.filter(order__in=today_orders).values('product__product__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        top_selling_variants_week = OrderItem.objects.filter(order__in=week_orders).values(
            'product__product__name',
            'product__size__size'
        ).annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]

        top_selling_variants_month = OrderItem.objects.filter(order__in=month_orders).values(
            'product__product__name',
            'product__size__size'
        ).annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')[:5]
        context = {
            'order_count_today': order_count_today,
            'total_price_today': total_price_today,
            'order_count_week': order_count_week,
            'total_price_week': total_price_week,
            'order_count_month': order_count_month,
            'total_price_month': total_price_month,
            'top_selling_variants_today': top_selling_variants_today,
            'top_selling_variants_week': top_selling_variants_week,
            'top_selling_variants_month': top_selling_variants_month,
        }


        template = 'adminside/sales_report_pdf.html'
        html_string = render_to_string(template, context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="sales_report.pdf"'

        pisa_status = pisa.CreatePDF(html_string, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response
    
    return redirect('signin')