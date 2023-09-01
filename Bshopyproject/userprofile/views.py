from django.shortcuts import render,redirect
from .models import *
from order.models import * 
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control

# Create your views here.
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def user_profile(request):
    user=request.user
    try:
        addresses=UserAdress.objects.filter(user=user)
    except ObjectDoesNotExist:
        addresses=None

    context={
        'addresses':addresses
    }
    return render(request,'userprofile/userprofile.html',context)

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def show_address(request):
    user=request.user
    try:
        addresses=UserAdress.objects.filter(user=user)

    except ObjectDoesNotExist:
        addresses=None
        return redirect('add-address')
    context={
        'addresses':addresses
    }
    return render(request,'userprofile/show_address.html',context)

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def add_address(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address_line_1=request.POST['address1']
        address_line_2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        postal_code=request.POST['pincode']
        country=request.POST['country']
        email=request.POST['email']
        phone_number=request.POST['phone']

        address=UserAdress(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address_line1=address_line_1,   
            address_line2=address_line_2,
            post_code=postal_code,
            city=city,
            state=state,
            country=country,
        )
        address.save()

        return redirect('show-address')
    
    return render(request,'userprofile/add_address.html')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_address(request,address_id):
    address=UserAdress.objects.get(id=address_id)
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address_line_1=request.POST['address1']
        address_line_2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        postal_code=request.POST['pincode']
        country=request.POST['country']
        email=request.POST['email']
        phone_number=request.POST['phone']

        address.user=request.user
        address.first_name=first_name
        address.last_name=last_name
        address.address_line1=address_line_1
        address.address_line2=address_line_2
        address.city=city
        address.state=state
        address.post_code=postal_code
        address.country=country
        address.email=email
        address.phone_number=phone_number

        address.save()
        return redirect('order-address')
    return render(request,'order/edit_address.html',{'address':address})

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def order_address(request):
    # if request.user.is_authentcated:
        user=request.user
        try:
            addresses=UserAdress.objects.filter(user=user)
            if not addresses.exists():
                return redirect('no-address')
        except ObjectDoesNotExist:
            return HttpResponse('something went wrong.')
        return render(request,'order/oreder_address.html',{'addresses':addresses})

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def no_address(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address_line_1=request.POST['address1']
        address_line_2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        postal_code=request.POST['pincode']
        country=request.POST['country']
        email=request.POST['email']
        phone_number=request.POST['phone']

        

        address=UserAdress(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address_line1=address_line_1,   
            address_line2=address_line_2,
            post_code=postal_code,
            city=city,
            state=state,
            country=country,
            
        )
        address.save()

        return redirect('order-address')
    
    return render(request,'order/add_order_address.html')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def delete_address(request,address_id):
    try:
        user_address=UserAdress.objects.get(id=address_id)
        user_address.is_active=False
        user_address.save()

    except user_address.DoesNotExist:
        return HttpResponse('address not found.')
    return redirect('show-address')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def user_wallet(request):
    user_wallet=Wallet.objects.filter(user=request.user).first()
    transaction=WalletTransaction.objects.filter(wallet=user_wallet)
    if user_wallet is not None:
        balance=user_wallet.balance
    else:
        balance=0
    context={
        'wallet':user_wallet,
        'transaction':transaction,
        'user_balance':balance
    }
    return render(request,'userprofile/wallet.html',context)

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def edit_address_userside(request,address_id):
    address=UserAdress.objects.get(id=address_id)
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        address_line_1=request.POST['address1']
        address_line_2=request.POST['address2']
        city=request.POST['city']
        state=request.POST['state']
        postal_code=request.POST['pincode']
        country=request.POST['country']
        email=request.POST['email']
        phone_number=request.POST['phone']

        address.user=request.user
        address.first_name=first_name
        address.last_name=last_name
        address.address_line1=address_line_1
        address.address_line2=address_line_2
        address.city=city
        address.state=state
        address.post_code=postal_code
        address.country=country
        address.email=email
        address.phone_number=phone_number

        address.save()
        return redirect('show-address')
    return render(request,'userprofile/edit_address_userside.html',{'address':address})