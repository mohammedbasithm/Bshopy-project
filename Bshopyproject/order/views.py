from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from .models import *
from cart.models import *
from django.contrib import messages
from django.db.models import F,Sum
from userprofile.models import UserAdress
import razorpay
from django.conf import settings
from django.http import JsonResponse
from userprofile.models import Wallet,WalletTransaction
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def check_out(request,adres_id):
    cart = get_object_or_404(Cart, user=request.user)
    cartitems = CartItems.objects.filter(cart = cart)
    try:
        user_wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        # Create a new wallet for the user
        user_wallet = Wallet.objects.create(user=request.user)

    if cartitems:

        user_add = get_object_or_404(UserAdress, id=adres_id, user=request.user)
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = None
        
        items = CartItems.objects.filter(cart=cart)
        subtotal = items.aggregate(total_price=Sum('price'))['total_price'] or 0
        
        total_price = subtotal
        if cart and cart.coupon:
            coupon = get_object_or_404(Coupon, coupon_code=cart.coupon)
            coupon_price = coupon.coupon_price
            total_price = subtotal - coupon_price
        else:
            coupon_price=0
            total_price = subtotal-coupon_price
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
            total_discount=subtotal-(total_amount)
        else:
            total_discount=subtotal-total_amount
        total_price=total_price-total_discount
        if subtotal <=1000:
            total_price+=50
        context = {
            'cart':cart,
            'subtotal': subtotal,
            'user_address': user_add,
            'cart': cart,
            'total_price': total_price,
            'total_discount':total_discount,
            'coupon_price':coupon_price,
            'wallet_amount':user_wallet.balance
        }

        return render(request,'order/check_out.html',context)
    
    return redirect('shop')
 
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def place_order(request,order_id):
    user_addrss=get_object_or_404(UserAdress,id=order_id,user=request.user)
    cart=get_object_or_404(Cart,user=request.user)

    cart_item=CartItems.objects.filter(cart=cart)
    subtotal=cart_item.aggregate(total_price=Sum('price'))['total_price'] or 0

    total_price=subtotal
    if cart and cart.coupon:
        coupon = get_object_or_404(Coupon, coupon_code=cart.coupon)
        min_amount = coupon.coupon_price
        total_price = subtotal - min_amount
    else:
        total_price = subtotal
    total_amount=0  
    for item in cart_item:
        product=item.product
                    
        if product.discount_price:
            sale=product.discount_price*item.quandity
            
        else:
            sale=product.price*item.quandity
            
        total_amount+=sale
    total_discount=0
    if cart.coupon and cart.coupon.coupon_price:
        coupon=cart.coupon
        total_discount=subtotal-(total_amount)
    else:
        total_discount=subtotal-total_amount
    total_price=total_price-total_discount
    if subtotal <=1000:
        total_price+=50      
    order=Order.objects.create(
        user=request.user,
        address=user_addrss,
        total_price=total_price,
        payment_status='pending',
        order_status='Ordered',
        payment_method='CASH_ON_DELIVERY',
        return_period_expired=timezone.now()+timedelta(days=5)

    )
    if cart and cart.coupon:
        coupon = get_object_or_404(Cart, user=request.user)
        couponss = Coupon.objects.get(coupon_code=coupon.coupon)
        UserCoupon.objects.create(
            user=request.user,
            coupon=couponss,
            used=True,
            total_price=float(total_price)
        )
        coupon.coupon = None
        coupon.save()
    else:
        # Add any additional logic that should be executed when no coupon is used
        pass
    for item in cart_item:
        
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.price,
            quantity=item.quandity
        )
        variant=item.product
        variant.stock-=item.quandity
        variant.save()
        item.delete()
    return render(request,'order/order_placed.html')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def initiate_payment(request):
    if request.method == 'POST':
        # Retrieve the total price and other details from the backend
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItems.objects.filter(cart=cart)
    
        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        total_price = subtotal
        if cart and cart.coupon:
            coupon = get_object_or_404(Coupon, coupon_code=cart.coupon)
            min_amount = coupon.coupon_price
            total_price = subtotal - min_amount
        else:
            total_price = subtotal
        total_amount=0  
        for item in cart_items:
            product=item.product
                        
            if product.discount_price:
                sale=product.discount_price*item.quandity
                
            else:
                sale=product.price*item.quandity
                
            total_amount+=sale
        total_discount=0
        if cart.coupon and cart.coupon.coupon_price:
            coupon=cart.coupon
            total_discount=subtotal-(total_amount)
        else:
            total_discount=subtotal-total_amount
        total_price=total_price-total_discount
        if subtotal <=1000:
            total_price+=50

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment = client.order.create({

            'amount': int(total_price * 100),
            'currency': 'INR', 
            'payment_capture': 1
              
            })
       
    
        response_data = {
            'order_id': payment['id'],
            'amount': payment['amount'],
            'currency': payment['currency'],
            'key': settings.RAZOR_KEY_ID,

        }
        return JsonResponse(response_data)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method'})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def online_payment_order(request, add_id):
    
    if request.method == 'POST':
        payment_id = request.POST.getlist('payment_id')[0]
        orderId = request.POST.getlist('orderId')[0]
        signature = request.POST.getlist('signature')[0]
        user_address = get_object_or_404(UserAdress, id=add_id, user=request.user)
        cart = Cart.objects.get(user_id=request.user)
        cart_items = CartItems.objects.filter(cart=cart)

        subtotal = cart_items.aggregate(total_price=Sum('price'))['total_price'] or 0
        total_price=subtotal
        if cart and cart.coupon:
            coupon = get_object_or_404(Coupon, coupon_code=cart.coupon)
            min_amount = coupon.coupon_price
            total_price = subtotal - min_amount
        else:
            total_price = subtotal
        total_amount=0  
        for item in cart_items:
            product=item.product
                        
            if product.discount_price:
                sale=product.discount_price*item.quandity
                
            else:
                sale=product.price*item.quandity
                
            total_amount+=sale
        total_discount=0
        
        if cart.coupon and cart.coupon.coupon_price:
            coupon=cart.coupon
            total_discount=subtotal-(total_amount)
        else:
            total_discount=subtotal-total_amount
        total_price=total_price-total_discount
        if subtotal <=1000:
            total_price+=50
        
        order = Order.objects.create(
            user=request.user,
            address=user_address,
            total_price=total_price,
            payment_status='Paid',
            payment_method='razorpay',
            order_status='Ordered',
            order_date=timezone.now(),
            razor_pay_payment_id=payment_id,
            razor_pay_payment_signature=signature,
            razor_pay_order_id=orderId,
            return_period_expired=timezone.now()+timedelta(days=5)
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quandity
            )
            variant = cart_item.product
            variant.stock -= cart_item.quandity
            variant.save()

        cart_items.delete()
        orderId = order.id


        return JsonResponse({'message': 'Order placed successfully', 'orderId': orderId})
    else:
        # Handle invalid request method (GET, etc.)
        return JsonResponse({'error': 'Invalid request method'})
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_success(request):
    return render(request,'order/order_placed.html')
from django.core.paginator import Paginator
def order(request):
    orders=Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(orders, 9)  # Display 9 categories per page
    page_number = request.GET.get('page')
    products_paginator = paginator.get_page(page_number)
    return render(request,'userprofile/order_list.html',{'orders':products_paginator})

def order_view(request,order_id):
    orderr=Order.objects.get(id=order_id)
    order_item=OrderItem.objects.filter(order=orderr)
    current_date=timezone.now()
    
    context={
        'order':orderr,
        'order_item':order_item,
        'current_date':current_date,
    }
    return render(request,'userprofile/order_view.html',context)
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)    
    if order.order_status != 'Cancelled':
        if order.payment_method in ['razorpay', 'Wallet pay']:
            user_wallet = Wallet.objects.get(user=request.user)
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
        if order.payment_status == 'Pending':
            order.payment_status='No payment'
        else:
            order.payment_status='Refunded'
        order.order_status='Cancelled'
        order.cancelled_date=timezone.now()
        order.save()
        
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            variant = item.product
            variant.stock += item.quantity
            variant.save()

        
    return redirect(request.META.get('HTTP_REFERER'))

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def return_request(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.order_status != 'Cancelled':  # The error might be here, incorrect status check.
        order.order_status = 'requested for return'
        order.payment_status='refund in progress'
        order.return_request_date = timezone.now()
        order.save()

    return redirect(request.META.get('HTTP_REFERER'))
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def pay_wallet(request,order_id):
    
    user_addrss=get_object_or_404(UserAdress,id=order_id,user=request.user)
    cart=get_object_or_404(Cart,user=request.user)

    cart_item=CartItems.objects.filter(cart=cart)
    subtotal=cart_item.aggregate(total_price=Sum('price'))['total_price'] or 0

    total_price=subtotal
    if cart and cart.coupon:
        coupon = get_object_or_404(Coupon, coupon_code=cart.coupon)
        min_amount = coupon.coupon_price
        total_price = subtotal - min_amount
    else:
        total_price = subtotal
    total_amount=0  
    for item in cart_item:
        product=item.product
                    
        if product.discount_price:
            sale=product.discount_price*item.quandity
            
        else:
            sale=product.price*item.quandity
            
        total_amount+=sale
    total_discount=0
    if cart.coupon and cart.coupon.coupon_price:
        coupon=cart.coupon
        total_discount=subtotal-(total_amount)
    else:
        total_discount=subtotal-total_amount
    total_price=total_price-total_discount
    if subtotal <=1000:
        total_price+=50      
    order=Order.objects.create(
        user=request.user,
        address=user_addrss,
        total_price=total_price,
        payment_status='pending',
        order_status='Ordered',
        payment_method='Wallet pay',
        return_period_expired=timezone.now()+timedelta(days=5)

    )
    if cart and cart.coupon:
        coupon = get_object_or_404(Cart, user=request.user)
        couponss = Coupon.objects.get(coupon_code=coupon.coupon)
        UserCoupon.objects.create(
            user=request.user,
            coupon=couponss,
            used=True,
            total_price=float(total_price)
        )
        coupon.coupon = None
        coupon.save()
    else:
        # Add any additional logic that should be executed when no coupon is used
        pass
    user_wallet = Wallet.objects.get(user=request.user)

    if user_wallet.balance >= total_price:
        user_wallet.balance -= total_price
        user_wallet.save()
    transaction_type = 'Purchased'
    WalletTransaction.objects.create(
        wallet=user_wallet,
        amount=total_price,
        order_id=order,
        transaction_type=transaction_type,
    )
    for item in cart_item:
        
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.price,
            quantity=item.quandity
        )
        variant=item.product
        variant.stock-=item.quandity
        variant.save()
    
    item.delete()
    return render(request,'order/order_placed.html')





