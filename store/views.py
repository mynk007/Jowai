from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, CustomerForm, ChangeProfilePicture
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy





class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('log_in')

# Create your views here.

def store(request):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, user_name=request.user ,complete=False)
          cartItems = order.get_cart_items
          CustomerObject=Customer.objects.get(user=request.user)
          user_pic=CustomerObject.profile_pic
     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          cartItems=[]
          log_status=False
          user_pic=''

     products=Product.objects.all()
     context = {'products': products, 'cartItems': cartItems, 'log_status': log_status, 'user_pic': user_pic}

     return render(request, 'store/Store.html', context)

@login_required(login_url="log_in")
def cart(request):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_item_set.all()
          cartItems = order.get_cart_items
     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          cartItems=[]
          log_status=False     
     
     context={'items': items, 'order': order, 'cartItems': cartItems, 'log_status': log_status}
     return render(request, 'store/Cart.html', context)

def checkout(request):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_item_set.all()
          cartItems = order.get_cart_items

     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          cartItems = []
          log_status=False
          items=[]


     context={'items': items, 'order': order, 'cartItems': cartItems, 'log_status': log_status}
     return render(request, 'store/Checkout.html', context)

def about(request):
     if request.user.is_authenticated:
          log_status=True
          customer=request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          cartItems = []
          log_status=False
     context={'order': order, 'cartItems': cartItems, 'log_status': log_status}

     return render(request, 'store/about.html', context)

def contact(request):
     if request.user.is_authenticated:
          log_status=True
          customer=request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          log_status=False
          cartItems=[]
          items=[]
     context={'order': order, 'cartItems': cartItems, 'log_status': log_status}

     return render(request, 'store/Contact.html', context)
def updateItem(request):
     print(request.body)
     data=json.loads(request.body)
     productId=data['productId'] 
     action=data['action']
     customer=request.user.customer
     product=Product.objects.get(id=productId)
     order,created = Order.objects.get_or_create(customer=customer, complete=False)
     orderItem, created=Order_Item.objects.get_or_create(order=order, product=product)
     print(orderItem)
     if action == 'add':
          orderItem.quantity=orderItem.quantity + 1
     elif action == 'remove':
          orderItem.quantity=orderItem.quantity - 1
     orderItem.save()
     if orderItem.quantity <= 0:
          orderItem.delete()
     return JsonResponse('Item Was Added', safe=False)

def processOrder(request):
     order_id=datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     if request.user.is_authenticated:
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer,complete=False)
          total = float(data['form']['total'])
          shipping_address = data['form']['address']+", "+data['form']['city']+", "+data['form']['state']+", "+data['form']['zipcode']
          product_details=[]
          price=data['item_price']
          name=data['item_names']
          qty=data['item_qty']
          contact_no=data['form']['contact_no']
          customer_name=data['form']['name']
          customer_email=data['form']['email']
          for i in range(0,len(name)):
               product_details.append("Name: "+name[i]+" , Qty: "+qty[i]+" , Price: "+price[i])
               i+=1
          order.product_details=product_details
          order.shipping_address=shipping_address
          order.order_id=order_id
          order.contact_no=contact_no
          order.user_email=customer_email
          # print(data['form']['address'])
          if total == order.get_cart_total:
               order.complete = True
          order.save()
          
          id=data['item_id']
          price=data['item_price']
          name=data['item_names']
          qty=data['item_qty']
          img=data['item_img']
          for i in range(0,len(name)):
              MyOrder.objects.create(name=name[i], quantity=qty[i], price=price[i], image=img[i], customer=request.user, product_id=id[i], order_id=order_id, shipping_address=shipping_address, customer_name= customer_name, customer_email= customer_email)
          
 
     return JsonResponse('Payment Completed', safe=False)

def myOrders(request):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
          myOrders=MyOrder.objects.filter(customer=request.user)
     else:
        cartItems = []
        order={'get_cart_items':0, 'get_cart_total':0}
        myOrders=[]
        log_status=False
              
     context={'myOrders': myOrders, 'cartItems':cartItems, 'log_status': log_status}
     return render(request, 'store/myOrders.html',context)

def order_details(request , id):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order_details=MyOrder.objects.get(id=id)
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
     else:
        cartItems = []
        order_details={'get_cart_items':0, 'get_cart_total':0}
        order_details=[]
        log_status=False
              
     context={'order_details': order_details, 'cartItems':cartItems, 'log_status': log_status}
     return render(request, 'store/OrderDetails.html', context)

def viewProduct(request, id):
     if request.user.is_authenticated:
          log_status=True
          customer = request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.order_item_set.all()
          cartItems = order.get_cart_items
     else:
        items = []
        cartItems=[]
        order={'get_cart_items':0, 'get_cart_total':0}
        log_status=False
     product = Product.objects.get(id=id)
     context = {'product':product, 'cartItems':cartItems, 'log_status': log_status}
     return render(request, 'store/viewProduct.html', context)

def register(request):
     form=CreateUserForm

     if request.method == 'POST':
          form=CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               user= form.cleaned_data.get('username')
               # userObject=User.objects.get(username=user)
               # print(userObject)
               first_name= form.cleaned_data.get('first_name')
               last_name= form.cleaned_data.get('last_name')
               contact_no=request.POST.get('contact_no')
               name=first_name+" "+last_name
               email= form.cleaned_data.get('email')
               userInstance=User.objects.get(username=user)
               Customer.objects.create(user=userInstance, name=name, email=email, contact_no=contact_no)

               messages.success(request, "User Registration Successful for " + user)
               return redirect('log_in')
     context ={'form': form}
     return render(request, 'store/Register.html', context)

def log_in(request):
     if request.user.is_authenticated:
          return redirect(store)

     else:
          if request.method == 'POST':
               username=request.POST.get('username')
               password=request.POST.get('password')
               user=authenticate(request, username=username, password=password)
               if user is not None:
                    login(request, user)
                    return redirect(store)
               else:
                    messages.info(request, "Username and Password is Incorrect")
               


          return render(request, 'store/Login.html')
def log_out(request):
     order=Order.objects.get(user_name=request.user.username, complete=False)
     # print(order)
     # order.delete()
     logout(request)

     return redirect('store')

def my_profile(request):
     customer=request.user.customer
     if request.user.is_authenticated:
          form=ChangeProfilePicture(instance=customer)
     
          if request.method=='POST':
               form=ChangeProfilePicture(request.POST, request.FILES, instance=customer)
               if form.is_valid():
                    print("form validation successful")
                    form.save()
          log_status=True
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
          name=request.user.first_name+" "+request.user.last_name
          user_name=request.user.username
          email=request.user.email
          CustomerObject=Customer.objects.get(user=request.user)
          user_pic=CustomerObject.profile_pic
          contact_no=CustomerObject.contact_no

     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          log_status=False
          items=[]

     context={'cartItems':cartItems, 'log_status': log_status, 'name':name, 'user_name':user_name, 'email':email, 'user_pic':user_pic, 'contact_no':contact_no, 'form': form}
     return render(request, 'store/profile.html', context)


def edit_profile(request):
     if request.user.is_authenticated:
          log_status=True
          customer=request.user.customer
          order,created = Order.objects.get_or_create(customer=customer, complete=False)
          cartItems = order.get_cart_items
          name=request.user.first_name+" "+request.user.last_name
          user_name=request.user.username
          email=request.user.email
          CustomerObject=Customer.objects.get(user=request.user)
          user_pic=CustomerObject.profile_pic


          if request.method == 'POST':
               username=request.user.username
               email=request.POST.get('email')
               first_name=request.POST.get('first_name')
               last_name=request.POST.get('last_name')
               contact_no=request.POST.get('contact_no')
               password=request.POST.get('password')

               user=authenticate(request, username=username, password=password)
               if user is not None:
                    user.email=email
                    user.first_name=first_name
                    user.last_name=last_name
                    user.save()
                    user.customer.contact_no=contact_no
                    user.customer.save()
                    return redirect(my_profile)
 
               else:
                    messages.info(request, "Password is Incorrect")



     else:
          order={'get_cart_items':0, 'get_cart_total':0}
          log_status=False
          items=[] 
     context={'cartItems':cartItems, 'log_status': log_status, 'name':name, 'user_name':user_name, 'email':email, 'user_pic':user_pic}
     return render(request, 'store/Edit_Profile.html', context)

     
def forgot_password(request):
     form=CreateUserForm

     if request.method == 'POST':
          form=CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               user= form.cleaned_data.get('username')
               # userObject=User.objects.get(username=user)
               # print(userObject)
               first_name= form.cleaned_data.get('first_name')
               last_name= form.cleaned_data.get('last_name')
               contact_no=request.POST.get('contact_no')
               name=first_name+" "+last_name
               email= form.cleaned_data.get('email')
               userInstance=User.objects.get(username=user)
               Customer.objects.create(user=userInstance, name=name, email=email, contact_no=contact_no)

     return render(request, 'store/forgot.html')


          

