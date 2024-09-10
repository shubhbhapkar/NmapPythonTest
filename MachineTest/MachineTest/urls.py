"""
URL configuration for MachineTest project.

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
from Machine import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #url for the login
    path('login/', views.SessionLoginView.as_view()),

    #url for the logout you need to make request to logout
    path('logout/', views.SessionLogoutView.as_view()),

    #url to see all clients
    path('GET/clients/', views.ClientListView.as_view()),

    #url to create client
    path('POST/clients/', views.ClientCreateView.as_view()),

    #url to see particulat client
    path('GET/clients/<int:id>/', views.ClientDetailView.as_view()),

    #url to update a client
    path('PUT-PATCH/clients/<int:id>/', views.ClientUpdateView.as_view()),

    #url to delete a client
    path('DELETE/clients/<int:id>/', views.ClientDeleteView.as_view()),

    #url to create project 
    path('POST/clients/<int:id>/projects/', views.ProjectCreateView.as_view()),

    #url to get projects assigned to the logged in user
    path('GET/projects/', views.UserAssignedProjectsView.as_view()),

   
]
