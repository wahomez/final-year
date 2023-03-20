"""gas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("ticket/", views.ticket, name="ticket"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("profile-form/", views.profile_form, name="profile-form"),
    # path("predict/", views.predict, name="predict"),
    path("checkout/<str:pk>/", views.checkout_page, name="checkout"),
    path('paypal-test/<int:pk>', views.create_payment, name='paypal-test'),
    path('paypal/execute_payment/', views.execute_payment, name='paypal-test/execute'),
    path('paypal/cancel_payment/', views.cancel_payment, name='paypal-test/cancel'),
    path("account/", views.account_page, name="account"),
    path("update-item/", views.updateItem, name="update-item"),
    path("order-history/", views.order_history, name="order-history"),
    path("logout/", views.logout_page, name="logout"),
]
