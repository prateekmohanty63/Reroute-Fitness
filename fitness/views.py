from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse
#from .models import Events
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from  django.views.decorators.csrf import csrf_exempt
from .models import Events
from django.core.mail import send_mail

from fitness.models import Events
from .PayTm import Checksum
MERCHANT_KEY='kbzk1DSbJiV_03p5'

# Create your views here.
def index(request):
    return render(request,'index.html')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        company=request.POST['company']
        mail=request.POST['email']
        phone=request.POST['phone']
        to=["reroute@gmail.com"]
        message=request.POST['message']
        subject = "User Tried to Contact"
        email_template_name = "contact_info_mail.txt"
        c = {
        "email":mail,
        "mobile":phone,
        "company":company,
        'domain':'127.0.0.1:8000',
        'site_name': 'Website',
        "user": name,
        'msg':message,
        }
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, 'dbmsprojekt@gmail.com' , ['reroutefitness@gmail.com'], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/')
    else:
        return render(request,"contact.html")

def register(request):
    if request.method=="POST":
        print(5)
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email is taken")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save();
                print(1)
                return redirect('login')
        else:
            messages.info(request,"Password not matching")
            return redirect('register')
        
    else:
        return render(request,"register.html")

def login(request):
    print(100)
    if request.method=='POST':
        print(-1)
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Incorrect username or password")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def about(request):
    return render(request,'about.html')

def gallery(request):
    return render(request,'gallery.html')

# url for searching events
def search_event(request):
    if request.method=="POST":
        searched=request.POST['searched']
        searched=searched.upper()
        print(searched)
        events=Events.objects.filter(name__contains=searched)
        return render(request,'event_search_res.html',{'searched':searched,'events':events})
    return render(request,'event_search.html')
def search_prog(request):
    return render(request,'event_search_res.html')

def event(request):
    events=Events.objects.all()

    
    return render(request,"event.html",{'events':events})

def event_img(request):
    return render(request,'events_gallery.html')
def my_event(request):
    if request.user.is_authenticated:
         return render(request,"my_events.html",{})
    else:
        return render(request,"/")
   

# payment integration

def payment(request):
    

    #request paytm to transfer the amount to your account after payment by user
    param_dict={
        'MID':'VHLskh33374131769871',
        'ORDER_ID':'order_order_id',
        'TXN_AMOUNT':'1',
         'CUST_ID':'email',
         'INDUSTRY_TYPE_ID':'Retail',
          'WEBSITE':'WEBSTAGING',
          'CHANNEL_ID':'WEB',
          'CALLBACK_URL':'https://127.0.0.1:8000/firstapp/handlerequest/'
    }

    param_dict['CHECKSUMHASH']=Checksum.generate_checksum(param_dict,MERCHANT_KEY)
    return render(request,'paytm.html',{'param_dict':param_dict})
    return render(request,'payment_page.html')




@csrf_exempt
def handlerequest(request):
    form =request.POST
    response_dict={}
    for i in form.keys():
        response_dict[i]=form[i]
        if i=='CHECKSUMHASH':
            checksum=form[i]
    verify=Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('payment successfull')
        else:
            print('payment was not successful because'+ response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response':response_dict})

def index(request):
    return render(request,'index.html')


# Email sending

