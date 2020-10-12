from django.urls import path, include
from . import views

app_name = 'ride_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('create_ride', views.create_ride, name='create_ride'),
    path('ride/<int:ride_id>', views.ride, name='ride'),
    path('join_ride/<int:ride_id>', views.join_ride, name='join_ride'),
    path('update_ride/<int:ride_id>', views.update_ride, name='update_ride'),
    path('cancel_ride/<int:ride_id>', views.cancel_ride, name='cancel_ride'),
    path('delete_ride/<int:ride_id>', views.delete_ride, name='delete_ride'),
    path('charge/', views.charge, name='charge'),
]
