from django.urls import path
from django.contrib.auth.views import LogoutView
from users.apps import UsersConfig
from .views import RegisterView, CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="fly:product_list"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
