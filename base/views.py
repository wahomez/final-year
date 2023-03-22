from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from .models import Profile, Product, Order, Payment
from django.http import JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from .keys import * 
from datetime import datetime
import paypalrestsdk
import pickle
import json
import pandas as pd
from django.db.models import Count
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import base64
# import jsonify

# Create your views here.
def homepage(request):
    product = Product.objects.all()

    context = {
        "products" : product
    }

    return render(request, "index.html", context)

def stk_push(request, pk):
    #get payment details from form
    if request.method == "POST":
        mobile = request.POST["mobile"]
        amount = request.POST["amount"]
        print("KEY:", pk)
        order = Order.objects.get(order_id=pk)
        order_id = order.order_id
        print("ID:", order_id)
    #get access token
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = response.json()["access_token"]

    #get payment details
    # mobile = 254748373873
    # amount = 100
    # description = "Product 1"

    #create payment payload
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMzIwMjM1NTA2",
        "Timestamp": "20230320235506",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": "254" + mobile,
        "PartyB": 174379,
        "PhoneNumber": "254" + mobile,
        "CallBackURL": "https://api.darajambili.com/express-payment",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }
    #stk push api
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
    
    code = response.json()
    print(code)

    try:
        if code["ResponseCode"] == '0':
            print("Complete pin prompt sent to your device to complete payment!")
            order = Order.objects.get(order_id=order_id)
            payment = Payment.objects.create(user=order.user, order=order
            )
            payment.save()
            order.paid=True
            order.save()
            status = order.paid
            messages.success(request, ("Payment successfull"))
            return redirect("checkout", order_id)
        else:
            print("Failed transaction. Try again!")
    except:
        print("Code didn't work")
    # print("Token:", access_token)
    return HttpResponse("We are good")

def ticket(request):
    return render(request, "ticket.html")

def login_page(request):
    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You are logged in successfully"))
            return redirect("/")
        else:
            messages.error(request, ("There was an error when login in. Please try again!"))
            return redirect("login")
            
        
    return render(request, "login.html")

def register_page(request):
    form = RegistrationForm()

    if request.method =="POST" or None:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            form.save()
            user = authenticate(request, email=request.POST["email"], password=request.POST["password1"])
            if user is not None:
                login(request, user)
                messages.success(request, ("You have been registered successsfully!"))
                return redirect("/profile-form")



    context = {
        "form" : form
    }

    return render(request,"register.html", context)

def logout_page(request):
    logout(request)
    messages.success(request, ("You have logged out successfully"))
    return redirect("/login")

# #loading saved model
# with open("model_revised.pkl", 'rb') as f:
#     columns_to_drop = pickle.load(f)
#     columns_to_add = pickle.load(f)
#     model = pickle.load(f)

# def predict(request):
#     # profile = Profile.objects.get(user=request.user)
#     #loading input data from db
#     input_data = Profile.objects.values("gas_brand", "gas_size", "married", "household_number", "kids_number")
#     print(str(input_data))
#     #convert input data to pd
#     X = pd.DataFrame.from_records(input_data)
#     print("Initial Df: ", X)

#     #drop columns and add new ones
#     X = X.drop(columns= columns_to_drop)
#     X = X.assign(columns=columns_to_add)
#     print("After drop: ", X)

#     #make predictions
#     prediction = model.predict(X)

#     #return prediction as Json
#     return JsonResponse({'prediction' : prediction.tolist()})

def profile_form(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    prediction = 30
    if request.method=="POST" or request.method=="FILES":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            try:
                profile2 = Profile.objects.get(user=request.user)
                # Assume you have retrieved the date string from the HTML form
                date_string = str(profile2.last_refill)
                print("Date 1:", date_string)

                # Convert the date string to a datetime object
                date = datetime.strptime(date_string, "%Y-%m-%d")
                print("Date 2:", date)

                # Add 20 days to the date
                new_date = date + timedelta(days=20)
                print("Date 3:", new_date)

                # Convert the new date back to a string in the desired format
                new_date_string = new_date.strftime("%Y-%m-%d")
                profile2.predicted_refill = new_date_string
                profile2.save()
                print(profile2.predicted_refill)
            except:
                print(KeyError)

            messages.success(request, ("You have successfully updated your profile"))
            return redirect("/")

    

    context = {
        "form" : form
    }

    return render(request, "profile.html", context)


@login_required(login_url="/login")
def checkout_page(request,pk):
    try:
        product = Product.objects.get(product_id=pk)
        order_instance = Order.objects.create(user=request.user, product=product)
        order_instance.save()
    except:
        order_instance = Order.objects.get(order_id=pk)
    order_id = order_instance.order_id
    product = order_instance.product
    print("Product:", order_id)
    price = product.price
    quantity = order_instance.quantity
    total = price * quantity

    order = Order.objects.filter(pk=order_id)
    paid = order_instance.paid
    print("Paid? ", paid)
    # items = Cart.objects.filter(user=request.user)
    # print(items)
    
    # item = order.product
    context = {
        "orders" : order,
        "price" : price,
        "total": total,
        "quantity": quantity,
        "order_id" : order_id,
        "paid" : paid
    }
    return render(request, "checkout.html", context)

def updateItem(request):
    return JsonResponse("Item was added", safe=False)

@login_required(login_url="/login")
def create_payment(request, pk):
    paypalrestsdk.configure(
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        mode= "sandbox"
    )
    order = Order.objects.get(order_id=pk)
    product = order.product.name
    price = order.product.price
    quantity = order.quantity
    total = price*quantity
    try:
        total_a = total_a*0.5
        print("Converted_total is :",total_a)
    except:
        pass
    order_id =str(order.order_id)
    print("Order ID:", order_id)
    if order.paid == True:
        messages.success(request, ("Your order has already been paid for!"))
        return redirect("checkout", pk)
    else:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/paypal/execute_payment/",
                "cancel_url": "http://localhost:8000/paypal/cancel_payment/"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": product,
                        "sku": order_id,
                        "price": price,
                        "currency": "USD",
                        "quantity": quantity
                    }]
                },
                "amount": {
                    "total": total,
                    "currency": "USD"
                },
                "description": "Transaction description.",
                "custom": order_id
            }]
        })
        if payment.create():
            for link in payment.links:
                if link.rel == 'approval_url':
                    return redirect(link.href)
        else:
            return HttpResponseServerError

@login_required(login_url="login")
def account_page(request):
    try:
        orders = Order.objects.filter(user=request.user).count()
    
    except:
        pass
    profile = Profile.objects.filter(user=request.user)

    context = {
        "profiles" : profile,
        "orders" : orders,
    }
    return render(request, "account.html", context)

  
@login_required(login_url="login")  
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    
    payment = paypalrestsdk.Payment.find(payment_id)
    booking_id = payment.transactions[0].custom
    print(booking_id)
    if payment.execute({"payer_id": payer_id}):
        order = Order.objects.get(order_id=booking_id)
        payment = Payment.objects.create(user=order.user, order=order
        )
        payment.save()
        order.paid=True
        order.save()
        status = order.paid
        print("sth:", status)
        return redirect("checkout", booking_id)

        # Payment successful, do something here
        # return HttpResponse("Payment worked")
    else:
        # Payment unsuccessful, do something here
        return HttpResponse("Payment failed")

def cancel_payment(request):
    messages.success(request, "You payment has been cancelled. Please try again!")
    return redirect("/")

def order_history(request):
    order = Order.objects.filter(user=request.user)
    context = {
        "orders" : order
    }
    return render(request, "cart.html", context)