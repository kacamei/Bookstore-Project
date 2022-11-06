from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
from .form import ImageForm
from .models import Image
from .models import Product
from django.db.models import Q
from .models import Coupon
from .form import CouponApplyForm
from django.utils import timezone
from django.views.decorators.http import require_POST
# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST['user_email']
        password = request.POST['user_password']

        user = auth.authenticate(username = email, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    
    else:
        return render(request, 'login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        username = request.POST['user_name']
        email = request.POST['user_email']
        password1 = request.POST['user_password']
        password2 = request.POST['user_password1']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.add_message(request, messages.INFO, 'Username taken')
                return redirect('register')


            elif User.objects.filter(email=email).exists():
                messages.add_message(request, messages.INFO, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username, password=password1, email=email, first_name=first_name,)
                user.save();

        else:
                print('password not matching')
                messages.add_message(request, messages.INFO, 'Password not matching')
        return redirect('/')
        

    else:
        return render(request,'register.html')




def logout(request):
    auth.logout(request)
    return redirect('/')

def SECONDPAGE(request):
    context = {}
    return render(request, 'SECONDPAGE.html', context)





def index(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'index.html', context)


def cart(request):


	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)


def check(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'check.html', context)




def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


def SearchPage(request):
    query = Q()
    results =[]
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(name__icontains=query) | Q(id__icontains=query) 

            results= Product.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'search page.html', context)

        else:
            return render(request, 'search page.html')

    else:
        return render(request, 'search page.html')



def upload(request):
    
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            obj=form.instance
            return render(request,"upload.html",{"obj":obj})  
    else:
        form=ImageForm()    
    img=Image.objects.all()
    return render(request,"upload.html",{"img":img,"form":form})


def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    
    coupon = Coupon.objects.get(code__iexact = code ,
                                valid_from__lte=now,
                                valid_to__gte=now,
                                active=True)
    request.session['coupon_id'] = coupon.id
    return redirect('cart:cart_detail')
