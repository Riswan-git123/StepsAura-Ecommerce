from .views import *
from django.urls import path


urlpatterns = [
    path("cart/",cart,name="cart"),
    path("details/<int:id>/",details,name="details"),
    path("contact/",contact,name="contact"),
    path("signup/",signup,name="signup"),
    path("login/",login,name="login"),
]
