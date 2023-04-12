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
    path("dashboard/", views.dashboard, name="dashboard"),
    path("stk-push/<str:pk>/", views.stk_push, name="stk-push"),
    path("stk-push/", views.stk_push2, name="stk-push2"),
    path("callback/", views.daraja_callback, name="mpesa-callback"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("profile-form/", views.profile_form, name="profile-form"),
    path("map/", views.map_view, name="map"),
    path("savings/", views.savings_page, name="savings"),
    path("G-pay/", views.G_pay, name="G-pay"),
    path("G-pay/<str:pk>/", views.G_pay2, name="G-pay2"),
    # path("map-directions/", views.directions, name="map-directions"),
    path("get-directions/<str:pk>/", views.pin_location, name="direction"),
    path("checkout/<str:pk>/", views.checkout_page, name="checkout"),
    path('paypal-test/<str:pk>', views.create_payment, name='paypal-test'),
     path('paypal-test/', views.create_payment2, name='paypal-test2'),
    path('paypal/execute_payment/', views.execute_payment, name='paypal-test/execute'),
    path('paypal/cancel_payment/', views.cancel_payment, name='paypal-test/cancel'),
    path("account/", views.account_page, name="account"),
    path("update-item/", views.updateItem, name="update-item"),
    path("order-history/", views.order_history, name="order-history"),
    path("order-detail/<str:pk>/", views.order_detail, name="order-detail"),
    path("logout/", views.logout_page, name="logout"),
]
