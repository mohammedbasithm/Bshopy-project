from datetime import datetime, timedelta
from django.utils import timezone
import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth import authenticate,login,logout
from  django.views.decorators.cache import cache_control
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import generate_token
from django.utils.crypto import get_random_string
from .models import UserProfile
from django.core.mail import send_mail





@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signup(request):
    
    if request.method == 'POST':
       
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'email already taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=pass1)

                user.save()

                messages.success(request,'your account has been successfully created')
                current_site = get_current_site(request)
                subject = 'Activate Your plant Account'
                message = render_to_string('confirmemail.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                user.email_user(subject,message)

                return render(request,'activation link.html')
        
        else:
            messages.info(request,'password not match')
            return redirect('signup')
       
    
    return render(request,'signup.html')
def activate(request,uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass1']


        user = authenticate(username=username, password=password)

        if user is not None :
         
        
            otp_store = get_random_string(length=5, allowed_chars='0123456789')
            request.session['otp'] = otp_store
            request.session['user_pk'] = user.pk
            print('Your otp:',otp_store)


            subject = "OTP Confirmations"
            message = f"Your OTP is: {otp_store}"

            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email]

            send_mail(subject, message, from_email,to_list, fail_silently = True )
            # login(request,user)
            # return redirect('home')

            return render(request,'otp.html') 
        else :
            messages.error(request, "Username or Password incorrect")  
            return redirect('signin')
      
      
    return render(request,'signin.html')

    
       
   
@cache_control(no_cache=True,no_store=True,must_revalidate=True)
def signout(request):
    if request.user.is_authenticated:
        logout(request)
    messages.error(request, 'logedout successfully')
    return redirect('home')


def otp_login(request):

    
    if request.method == 'POST':
        send_otp = request.session.get('otp')
        user_id = request.session.get('user_pk')
        store_otp = request.POST['otp']
        

        if send_otp == store_otp:
            myuser = User.objects.get(id=user_id)
            login(request, myuser)
            messages.success(request, "You are logedin")
            return redirect('home')
        else:
            messages.error(request, 'Oooppss Invalid OTP')
            return redirect('signin')
    messages.success(request, "we have sent an otp to your email")
    return render(request,'otp.html')

def home(request):
    return render(request,'home.html')

def generate_otp():
    # Generate a 6-digit random OTP
    return str(random.randint(100000, 999999))

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Handle case when the email is not found in the database
            return render(request, 'password_reset_request.html', {'error_message': 'Email not found'})

        # Create a UserProfile object and associate it with the user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        # Generate OTP and store it along with its expiration time in the UserProfile model
        otp = generate_otp()
        user_profile.otp = otp
        user_profile.otp_expiry = datetime.now() + timedelta(minutes=10)
        user_profile.save()

        # Send the OTP to the user's email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp}',
            'bshopyproject@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect('verify-otp')
    return render(request, 'forgot_password/resend_password.html')



def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        try:
            print( otp)
            userprofile = UserProfile.objects.get(otp=otp, otp_expiry__gte=timezone.now())
        except UserProfile.DoesNotExist:
            return render(request, 'password_reset/verification_otp.html', {'error_message': 'Invalid OTP'})

        # Store the userprofile in the session to use it in the reset_password view
        request.session['userprofile_id'] = userprofile.id

        return redirect('reset-password')
    return render(request, 'forgot_password/verification_otp.html')

def reset_password(request):
    if request.method == 'POST':
        pass1 = request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1==pass2:

            # Retrieve the userprofile from the session
            userprofile_id = request.session.get('userprofile_id')
            if userprofile_id is None:
                # Redirect to the verify_otp view if the userprofile is not found in the session
                return redirect('verify-otp')

            try:
                userprofile = UserProfile.objects.get(pk=userprofile_id)
            except UserProfile.DoesNotExist:
                # Redirect to the verify_otp view if the userprofile is not found in the database
                return redirect('verify-otp')

            # Get the associated user from the userprofile
            user = userprofile.user

            # Update the user's password with the new one
            user.set_password(pass1)
            user.save()

            # Clear the userprofile from the session after successful password reset
            del request.session['userprofile_id']

            return redirect('signin')  # Redirect to the login page or any other page
        else:
            messages.info(request,'password not match')
            return render(request, 'forgot_password/re_enter_password.html')
    return render(request, 'forgot_password/re_enter_password.html')