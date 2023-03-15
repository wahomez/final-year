from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from .models import Profile, Product, Order, Cart
from django.http import JsonResponse

# Create your views here.
def homepage(request):
    product = Product.objects.all()

    context = {
        "products" : product
    }

    return render(request, "index.html", context)

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

def profile_form(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method=="POST" or request.method=="FILES":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request, ("You have successfully updated your profile"))
            return redirect("/")

    

    context = {
        "form" : form
    }

    return render(request, "profile.html", context)


def cart_page(request):
    order = Order.objects.filter(user=request.user)
    item = Cart.objects.filter(user=request.user)
    context = {
        "orders" : order,
        "items" : item
    }
    return render(request, "cart.html", context)

def checkout_page(request):
    order = Order.objects.filter(user=request.user)
    # print(order)
    items = Cart.objects.filter(user=request.user)
    # print(items)
    
    # item = order.product
    context = {
        "orders" : order,
        "items" : items
    }
    return render(request, "checkout.html", context)

def updateItem(request):
    return JsonResponse("Item was added", safe=False)