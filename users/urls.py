from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView

urlpatterns = [

    path('profile/', views.profile_view, name='profile'),

    path('password/', PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/users/profile/'
    ), name='change_password'),

]