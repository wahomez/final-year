from django.contrib import admin
from .models import User, Profile, Order, Product, Payment, UserLocation

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(UserLocation)
