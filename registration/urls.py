"""
URL configuration for Registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel/add_user/', views.add_user, name='add_user'),
    path('admin_panel/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin_panel/delete_user/', views.delete_user, name='delete_user'),
    path('', views.signup_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('home/', views.home_page, name='home'),
    path('logout/', views.logout_page, name='logout'),
]
