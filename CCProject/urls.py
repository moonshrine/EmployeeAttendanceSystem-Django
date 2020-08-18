"""CCProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from MyWebsite.views import (
		login_view, 
        logout_view,
		admin_home_view, 
		admin_home_view2,
        employee_view, 
		register_user_view,
		update_profile_view,
		template_view,
        employee_entry_view
		)

urlpatterns = [
	path('',login_view, name="home"),
    path('logout/',logout_view, name="logout"),
	path('adminhome/',admin_home_view, name="adminhome"),
	path('adminhome2/',admin_home_view2, name="adminhome2"),
    path('adduser/',register_user_view, name="register"),
    path('update/',update_profile_view, name="update"),
    path('template1/',template_view, name="template"),
    path('admin/', admin.site.urls),
    path('entry/', employee_entry_view, name="entry"),
    path('employee/<int:id>/', employee_view, name="employee"),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password/password_change_done.html'),
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password/password_change.html'),
        name='password_change'),
    
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_done.html'),
        name='password_reset_done'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('reset/<uid64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),name='password_change_done'),
]
