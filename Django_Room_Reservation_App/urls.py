"""Django_Room_Reservation_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from reservation_app.views import NewRoom, Homepage, RoomList, DeleteRoom, ModifyRoom, NewReservation, RoomInfo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Homepage.as_view(), name='homepage'),
    path('room/new/', NewRoom.as_view()),
    path('room/list/', RoomList.as_view()),
    path('room/delete/<int:id>', DeleteRoom.as_view()),
    path('room/modify/<int:id>', ModifyRoom.as_view()),
    path('room/reserve/<int:id>',NewReservation.as_view()),
    path('room/info/<int:id>', RoomInfo.as_view() ),

]
