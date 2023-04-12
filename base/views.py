from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from .models import Profile, Product, Order, Payment, UserLocation, Invoice, Delivery, Saving, Transaction
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
from .maps import get_directions
from django.views.decorators.csrf import csrf_exempt
# import pandas as pd
from sklearn.preprocessing import StandardScaler
import googlemaps

def dashboard(request):
    context = {

    }
    return render(request, "dashboard.html", context)
def directions(request):
    # Get the user's location
    user_location = UserLocation.objects.filter(user=request.user).last()

    # Get the location of one of your shops (replace with your own data)
    shop_latitude = 37.7749
    shop_longitude = -122.4194

    # Call the get_directions function to get the directions
    directions_result = get_directions(f"{user_location.latitude}, {user_location.longitude}",
                                        f"{shop_latitude}, {shop_longitude}")

    # Render the template with the directions and map data
    context = {'directions': directions_result,
                'user_latitude': user_location.latitude,
                'user_longitude': user_location.longitude,
                'shop_latitude': shop_latitude,
                'shop_longitude': shop_longitude}
    return render(request, 'directions.html', context)

def pin_location(request, pk):
    gmaps = googlemaps.Client(key="AIzaSyDBq8Dq8LSysLUuMa80PVsOqO2ZA33AZWw")
    # origin = request.GET.get('origin')
    origin = "New+York+City"
    destination = '123 Main St, Anytown, USA'
    directions = gmaps.directions(origin, destination)
    delivery = Delivery.objects.get(order=pk)
    print("Delivery: ", delivery)
    if request.method == "POST":
        delivery.date = datetime.now()
        delivery.save()
        messages.success(request, ("Delivery done successful. Thank you for choosing us!"))
        return redirect("home")
        
    return render(request, 'pin_location.html', {'directions': directions})
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
        "CallBackURL": "https://a527-102-135-170-111.eu.ngrok.io/callback/",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of Gas" 
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

def stk_push2(request):
    #get payment details from form
    if request.method == "POST":
        mobile = request.POST["mobile"]
        amount = request.POST["amount"]
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
        "CallBackURL": "https://a527-102-135-170-111.eu.ngrok.io/callback/",
        "AccountReference": "Rureri Traders",
        "TransactionDesc": "Deposit for G-save" 
    }
    #stk push api
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
    
    code = response.json()
    print(code)

    account = Saving.objects.get(user=request.user)
    savings = account.balance
    amount = float(amount)

    try:
        if code["ResponseCode"] == '0':
            print("Complete pin prompt sent to your device to complete payment!")
            trans_type="deposit"
            recipient = "MPESA"
            details = "Deposit with Mpesa"
            transaction = Transaction.objects.create(user=request.user, trans_type=trans_type, recipient=recipient, details=details, amount=amount)
            transaction.save()
            account.balance = savings + amount
            account.save()
            messages.success(request, ("You have successfully deposited with Mpesa!"))
            # return redirect("savings")
            return redirect("savings")
        else:
            print("Failed transaction. Try again!")
    except:
        print("Code didn't work")
    # print("Token:", access_token)
    return HttpResponse("We are good")


@csrf_exempt
def daraja_callback(request):
    
    print("Working!")
    # Extract relevant data from the callback
    transaction_id = request.POST.get('TransID', '')
    transaction_status = request.POST.get('TransStatus', '')

    try:
        if request.method == 'POST':
            # Retrieve the JSON data from the request body
            callback_data = json.loads(request.body)

            # Check if the transaction was successful
            if callback_data.get('Body.stkCallback.ResultCode') == '0':
                # Handle the successful transaction
                print("Callback Data:", callback_data)

                # Return a success response
                response_data = {
                    'ResultCode': 0,
                    'ResultDesc': 'Success'
                }
                return HttpResponse(json.dumps(response_data), content_type='application/json')
            else:
                # Handle the failed transaction
                # ...
                print("Payment Cancelled!")

                # Return an error response
                response_data = {
                    'ResultCode': 1,
                    'ResultDesc': 'Error'
                }
                return HttpResponse(json.dumps(response_data), content_type='application/json')

        # Return a bad request response if the request method is not POST
        response_data = {
            'ResultCode': 1,
            'ResultDesc': 'Invalid request method'
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)
    except:
        print("Error!")

    # Perform any necessary actions, such as updating your database
    # ...

    # Return a response to Daraja
    return HttpResponse(status=200)

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


@login_required(login_url="login")
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
            try:
                with open("model_revised.pkl", 'rb') as f:
                    columns_to_add = pickle.load(f)
                    columns_to_drop = pickle.load(f)
                    model = pickle.load(f)
                    print("Model:", model)

                data = {
                    "Where do you stay?": request.POST.get("location"),
                    "What brand of LPG cylinder do you use?": request.POST.get("gas_brand"),
                    "What size is your cylinder?": request.POST.get("gas_size"),
                    "Using your gas cylinder, what cooking method do you mostly use?": request.POST.get("cooking_method"),
                    "Are you married?": request.POST.get("married"),
                    "Do you have kids in your household?": request.POST.get("kids_number"),
                }

                # Convert the input data to a Pandas DataFrame
                input_df = pd.DataFrame([data])
                print("DF:", input_df)

                # Apply the same preprocessing as used during training
                input_df = input_df.join(pd.get_dummies(input_df["Where do you stay?"]))
                input_df.drop("Where do you stay?", axis=1, inplace=True)

                input_df = input_df.join(pd.get_dummies(input_df["What brand of LPG cylinder do you use?"]))
                input_df.drop("What brand of LPG cylinder do you use?", axis=1, inplace=True)
                print("Cylinder:", input_df)

                married = pd.get_dummies(input_df['Are you married?'])
                married.columns = ["Married " + col for col in married.columns]
                input_df = input_df.join(married)
                print("Married:", input_df)

                kids = pd.get_dummies(input_df['Do you have kids in your household?'])
                kids.columns = ["Kids " + col for col in kids.columns]
                input_df = input_df.join(kids)
                print("Kids:", input_df)

                input_df.drop("Do you have kids in your household?", axis=1, inplace=True)
                input_df.drop("Are you married?", axis=1, inplace=True)
                print("Marriage Drop:", input_df)

                gas_size = input_df["What size is your cylinder?"].str.split(" ").apply(lambda x: x[0])
                print("size:", gas_size)
                input_df.drop("What size is your cylinder?", axis=1, inplace=True)
                input_df.join(gas_size)
                print("Size Drop:", input_df)

                methods = input_df["Using your gas cylinder, what cooking method do you mostly use?"].str.split("(").apply(lambda x: x[0])
                input_df = input_df.join(pd.get_dummies(methods))
                input_df.drop("Using your gas cylinder, what cooking method do you mostly use?", axis=1, inplace=True)
                print("Final DF:", input_df)

                # Scale the input data using the same scaler as used during training
                scaler = StandardScaler()
                input_scaled = scaler.fit_transform([input_df.iloc[0]])
                print("Scaled:", input_scaled)

                # Make predictions using the trained model
                prediction = model.predict(input_df)
                print("Predict:", prediction)

                # Return the prediction to the HTML template
                print("Prediction:", prediction)
            except:
                print("Model didn't work!")
            return redirect("/")

    

    context = {
        "form" : form
    }

    return render(request, "profile.html", context)

def G_pay(request):
    if request.method == "POST":
        order_id = request.POST["id"]
        order = Order.objects.get(order_id=order_id)
        amount = order.product.price
        store = order.product.store
        account = Saving.objects.get(user=request.user)
        savings = account.balance
        amount = float(amount)
        trans_type="payment"
        recipient = store
        details = f"Payment for Order Number:",{order_id}
        if savings > amount:
            transaction = Transaction.objects.create(user=request.user, trans_type=trans_type, recipient=recipient, details=details, amount=amount)
            transaction.save()
            account.balance = savings - amount
            account.save()
            # messages.success(request, ("You have successfully deposited with Mpesa!"))
            # order = Order.objects.get(order_id=order_id)
            payment = Payment.objects.create(user=order.user, order=order)
            payment.save()
            order.paid=True
            order.save()
            status = order.paid
            messages.success(request, ("Payment successfull"))
            return redirect("savings")
        else:
            messages.success(request, ("Insufficient funds. Please deposit and try again!"))
            return redirect("savings")

def G_pay2(request, pk):
    order = Order.objects.get(order_id=pk)
    store = order.product.store
    if request.method == "POST":
        amount = request.POST["amount"]
        account = Saving.objects.get(user=request.user)
        savings = account.balance
        amount = float(amount)
        trans_type="payment"
        recipient = store
        details = f"Payment for Order Number:",{pk}
        if savings > amount:
            transaction = Transaction.objects.create(user=request.user, trans_type=trans_type, recipient=recipient, details=details, amount=amount)
            transaction.save()
            account.balance = savings - amount
            account.save()
            # messages.success(request, ("You have successfully deposited with Mpesa!"))
            # order = Order.objects.get(order_id=order_id)
            payment = Payment.objects.create(user=order.user, order=order)
            payment.save()
            order.paid=True
            order.save()
            status = order.paid
            messages.success(request, ("Payment successfull"))
            return redirect("checkout", pk)
        else:
            messages.success(request, ("Insufficient funds. Please deposit and try again!"))
            return redirect("savings")

def savings_page(request):
    savings = Saving.objects.filter(user=request.user)
    transaction = Transaction.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user, completed=False)
    if request.method == "POST":
        savings = Saving.objects.create(user=request.user)
        savings.save()
        messages.success(request, ("You have successfully created a G-save account"))
        return redirect("savings")
    # order = Order.objects.get(user=request.user, completed=False)
    # order_id = order.order_id

    context = {
        "savings" : savings,
        "transactions": transaction,
        "orders": orders,
    }
    return render(request, "savings_page.html", context)

@login_required(login_url="/login")
def checkout_page(request,pk):
    try:
        product = Product.objects.get(product_id=pk)
        order_instance = Order.objects.create(user=request.user, product=product)
        order_instance.save()
    except:
        order_instance = Order.objects.get(order_id=pk)
    try:
        payment = Payment.objects.get(order=order_instance)
        # payment = 
        # print(payment)
        payment_date = payment.date
        # print("Date 1:", payment_date)
    except:
        print("Error in date")
    order_id = order_instance.order_id
    product = order_instance.product
    # print("Product:", product)
    price = product.price
    quantity = order_instance.quantity
    total = price * quantity
    profile = Profile.objects.get(user=request.user)
    refill_date = profile.last_refill

    order = Order.objects.filter(pk=order_id)
    paid = order_instance.paid

    date = order_instance.date_ordered


    
    print("Date:", refill_date)
    # print("Paid? ", paid)

    if request.method == "POST":
        first_name = request.POST['firstName']
        last_name = request.POST["lastName"]
        email = request.POST["email"]
        location = request.POST["location"]
        number = request.POST["number"]
        invoice = Invoice.objects.create(first_name=first_name, last_name=last_name, email=email, location=location, product=product, order_date=date, price=price, quantity=quantity, total=total)
        invoice.save()
        order_instance.completed = True
        order_instance.save()
        profile.last_refill = date
        profile.save()
        user = request.user
        delivery_point = user.profile.location
        print("Location:", delivery_point)

        date = datetime.now()
        delivery = Delivery.objects.create(user=user, delivery_point=delivery_point, order=order_instance)
        delivery.save()
        
        messages.success(request, ("Successfully completed checkout.Your invoice will be sent to your email shortly."))
        return redirect("order-detail", order_id)

        
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

def create_payment2(request):
    paypalrestsdk.configure(
        client_id= CLIENT_ID,
        client_secret= CLIENT_SECRET,
        mode= "sandbox"
    )
    if request.POST:
        amount=request.POST['amount']
    else:
        HttpResponse("Nothing here")
        
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
                        "name": "Deposit to G-save",
                        "sku": "Deposit",
                        "price": amount,
                        "currency": "USD",
                        "quantity": "1"
                    }]
                },
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Transaction description.",
                "custom": "Deposit"
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
    amount = payment.transactions[0].amount.total
    account = Saving.objects.get(user=request.user)
    savings = account.balance
    amount = float(amount)
    # print("Savings", type(savings))
    # print("Amount", type(amount))
    # print(amount)
    if payment.execute({"payer_id": payer_id}):
        if booking_id =="Deposit":
            trans_type="deposit"
            recipient = "PAYPAL"
            details = "Deposit from Paypal"
            transaction = Transaction.objects.create(user=request.user, trans_type=trans_type, recipient=recipient, details=details, amount=amount)
            transaction.save()
            account.balance = savings + amount
            account.save()
            messages.success(request, ("You have successfully deposited from PayPal!"))
            return redirect("savings")
        else:
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

@login_required(login_url="login")
def order_history(request):
    order = Order.objects.filter(user=request.user)
    context = {
        "orders" : order
    }
    return render(request, "cart.html", context)
def order_detail(request, pk):
    order1 = Order.objects.get(order_id=pk)
    # delivery = 
    # print("Del", delivery)
    order = Order.objects.filter(order_id=pk)
    context = {
        "order" : order
    }
    return render(request, "order_detail.html", context)
def map_view(request):
    return render(request, 'maps.html')
