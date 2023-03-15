from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils import timezone

#location
LOCATION_CHOICES = [
    ("Nairobi", "Nairobi"),
    ("Mombasa", "Mombasa"),
    ("Mt Kenya", "Mt Kenya"),

]

GAS_CHOICES = [
    ("K-gas", "K-gas"),
    ("Total", "Total"),
    ("Progas", "Progas"),
]

SIZE_CHOICES = [
    ("6kgs", "6kgs"),
    ("13kgs", "13kgs"),
]

SEQUENCE_CHOICES = [
    ("Microwaving", "Microwaving"),
    ("Stir-frying", "Stir-frying"),
    ("Broiling", "Broiling"),
    ("Steaming", "Steaming"),
    ("Baking", "Baking"),
    ("Roasting", "Roasting"),
    ("Boiling", "Boiling"),
    ("Simmering", "Simmering"),
]

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE, null=True)
    pic = models.ImageField(default="profile.png", null=True)
    mobile_number = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=200, choices=LOCATION_CHOICES, null=True)
    gas_brand = models.CharField(max_length=200, choices=GAS_CHOICES, null=True)
    gas_size = models.CharField(max_length=20, choices=SIZE_CHOICES, null=True)
    married = models.BooleanField(default=False, null=True)
    household_number = models.IntegerField(null=True)
    kids_number = models.IntegerField(default=0, null=True)
    kids_below3 = models.IntegerField(default=0, null=True)
    cooking_sequence = models.IntegerField(null=True)
    cooking_method = models.CharField(max_length=200, choices=SEQUENCE_CHOICES, null=True)
    last_refillspan = models.IntegerField(null=True)
    updated = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.user.username
    
#Autogenerate Profile after User SignUp
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Product(models.Model):
    category = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    pic = models.ImageField()
    size = models.CharField(max_length=20)
    store = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.name) + str(" ") + str(self.size)

        

class Order(models.Model):
    user = models.ForeignKey(User, related_name="order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_ordered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + str(" - ") + str(self.product)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class Cart(models.Model):
    user = models.ForeignKey(User, related_name="cartuser", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="cartorder", on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + str("-") + str(self.order)

    @property
    def get_cart_total(self):
        try:
            print(" hello 1")
            items = []
            items.append(item for item in self.order)
            print(" hello")
            # total = sum(item.get_total for item in int(self.order))
            # print(total)
            # return total
        except:
            print("error")
        
    @property
    def get_cart_items(self):
        cartorders = self.order
        total = sum(item.quantity for item in cartorders)
        return total

    
class Payment(models.Model):
    user = models.ForeignKey(User, related_name="payment", on_delete=models.CASCADE)
    method =models.CharField(max_length=200)
    total_amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user) + str("-") + str(self.date)



