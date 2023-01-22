from django.urls import path
from . import views
from django.contrib.auth import views as authviews
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(views.HomeListView.as_view()), name="home"),
    path("signup/", views.SignUp.as_view(), name="signup"),
    path('login/',authviews.LoginView.as_view(redirect_authenticated_user=True,template_name="login.html")),
    path('logout/',authviews.LogoutView.as_view(template_name="logout.html")),
]
