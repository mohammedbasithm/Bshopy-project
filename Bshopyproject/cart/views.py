from django.shortcuts import get_object_or_404,render,redirect
from .models import *
from django.http import HttpResponseRedirect,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def cart(request):
    if request.user.is_authenticated:
            cart=get_object_or_404(Cart,user=request.user)
            cartitems=CartItems.objects.filter(cart=cart)
            if cart.cartitems_set.count()==0:
                cart.coupon=None
                cart.save()
            if cartitems:
                original_total_price=cart.get_total_price()
                sub_total=original_total_price
                
                if  request.method=='POST':
                    coupon_code=request.POST['coupon']
                    try:
                        coupon=Coupon.objects.get(coupon_code=coupon_code)
                        usercoupon=UserCoupon.objects.filter(coupon=coupon,user=request.user)
                        if not coupon.is_expired and original_total_price>=coupon.minimum_amount and not usercoupon.exists():
                            cart.coupon=coupon
                            cart.save()

                            messages.success(request,'coupon applied successfully.')
                        else:
                            messages.error(request,'coupon already applied.')

                        return redirect('cart')
                    except ObjectDoesNotExist:
                        messages.error(request,'coupon does not exist.')

                        return redirect('cart')
                if cart.coupon:
                    coupon=cart.coupon
                    total_price=cart.get_total_price()
                    total_price-=coupon.coupon_price
                    coupon_price=coupon.coupon_price
                else:
                    total_price=original_total_price
                    coupon_price=0 
                total_amount=0  
                for item in cartitems:
                    product=item.product
                    
                    if product.discount_price:
                        sale=product.discount_price*item.quandity
                    else:
                        sale=product.price*item.quandity
                    total_amount+=sale
                total_discount=0
                if cart.coupon and cart.coupon.coupon_price:
                    coupon=cart.coupon
                    total_discount=sub_total-(total_amount)
                else:
                    total_discount=sub_total-total_amount
                total_price=total_price-total_discount
                context = {
                'cart_items': cartitems,
                'user_cart': cart,
                'total_price':sub_total,
                'total_discount':total_discount,
                'total_amount':total_price,
                'coupon_price':coupon_price,
                }
                return render(request, 'cart/cart.html', context)
            return render(request, 'order/no_cart.html')
         
    else:
        return render(request,'signin.html')
   
def add_to_cart(request, selected_variant_id):
    if request.user.is_authenticated:
        try:
            product_variant = ProductVariant.objects.get(id=selected_variant_id)

            # Check if a cart exists for the user, or create a new one
            cart, created = Cart.objects.get_or_create(user=request.user)

            item = cart.cartitems_set.filter(product=product_variant).first()
            

            if item:
                available_stock=product_variant.stock-item.quandity
                request_quandity=1

                if available_stock>=request_quandity:
                    item.quandity += request_quandity
                    item.save()
                    messages.success(request,'item add to cart.')
                else:
                    messages.error(request,'Requested quantity exceeds available stock')
            else:
                if product_variant.stock>=1:
                    
                    CartItems.objects.create(cart=cart, product=product_variant, quandity=1, price=product_variant.price)
                    messages.success(request,'item add to cart.')

                else:
                    messages.error(request,'Requested quantity exceeds available stock')

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        except ProductVariant.DoesNotExist:
            # Handle the case where the ProductVariant does not exist
            return render(request,'productdetails.html')
    else:
        return redirect('signin')


def remove_from_cart(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            item_id=request.POST.get('item_id')
            cart_item=CartItems.objects.get(id=item_id)
            cart_item.delete()
        return HttpResponseRedirect('cart') 
    return render(request,'signin.html')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        user_products=CartItems.objects.filter(cart__user=request.user).values_list('product__id',flat=True)
        items=WishlistItem.objects.filter(wishlist=wishlist)
        context={
                'wishlist':wishlist,
                'items':items,
                'user_products':user_products,
            }
        return render(request,'cart/wish_list.html',context)
    return render(request,'signin.html')


def add_to_wishlist(request, variant_id):
    if request.user.is_authenticated:
        variant = ProductVariant.objects.get(id=variant_id)

        # Get or create the user's wishlist
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)

        # Check if the item already exists in the wishlist
        item, item_created = WishlistItem.objects.get_or_create(wishlist=wishlist, product=variant)

        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return render(request,'signin.html')

def update_quantity(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')
            
            product = CartItems.objects.get(id=product_id)
            product.quandity = quantity
            product.price = product.product.price * Decimal(product.quandity)
            product.save()
            
            user_cart = Cart.objects.get(user=request.user)
            total_price=0
            total_amount=0
            sub_total=0
            cart_items = user_cart.cartitems_set.all()

            for item in cart_items:
                product=item.product
                total_price=product.price*item.quandity
                sub_total=sub_total+total_price

                if product.discount_price:
                    sale=product.discount_price*item.quandity
                else:
                    sale=product.price*item.quandity
                total_amount=total_amount+sale
            
            if user_cart.coupon:
                coupon=user_cart.coupon
                coupon_price=coupon.coupon_price
                total_amount-=coupon_price

            else:
                coupon_price=0 
                total_amount-=coupon_price        
            total_discount=0
                
            total_discount=sub_total-total_amount-coupon_price
            # Prepare the response data
            response_data = {
                'success': True,
                'message': 'Quantity updated successfully!',
                'price': str(product.price),
                'total_price': str(sub_total),
                'total_discount':str(total_discount),
                'total_amount':str(total_amount),
                'coupon_price':str(coupon_price),
            }

            return JsonResponse(response_data)
        
        response_data = {
            'success': False,
            'message': 'Invalid request',
        }
        
        return JsonResponse(response_data, status=400)
    return render(request,'signin.html')
def remove_coupon(request):
    if request.user.is_authenticated:
        carts = Cart.objects.get(user =request.user)
        carts.coupon = None
        carts.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request,'signin.html')
  
def remove_wishlist(request,variant_id):
    if request.user.is_authenticated:
        variant=ProductVariant.objects.get(id=variant_id)
        wishlist=Wishlist.objects.get(user=request.user)
        item=wishlist.wishlistitem_set.filter(product=variant)

        if item.exists():
            item.delete()

        return redirect('wish-list')
    return render(request,'signin.html')