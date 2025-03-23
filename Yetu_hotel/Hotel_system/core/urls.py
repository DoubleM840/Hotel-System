# myapp/urls.py

from django.urls import path
from . import views
from .views import available_rooms, room_details, home, book_room, booking_success,PaymentSuccessView,payment_success

urlpatterns = [
    path('', home, name='home'),  # Assuming you have a home view
    # Login route
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('rooms/', available_rooms, name='rooms'),  # Add this line
    path('rooms/<int:room_id>/', room_details, name='room_details'),  # For room details
    path('book/<int:room_id>/', book_room, name='book_room'),  # URL for booking a room
    path('booking-success/', booking_success, name='booking_success'),  # URL for booking success
    path('payment/<int:booking_id>/', views.payment_view, name='process_payment'),  # Ensure name is 'process_payment
    path('payment-success/<int:id>/', views.payment_success, name='payment_success'),
      path('payment/success/<int:payment_id>/', PaymentSuccessView.as_view(), name='payment_success'),  # URL for payment success
      path('dashboard/', views.dashboard, name='dashboard'),
      path('generate_receipt/<int:booking_id>/', views.generate_receipt, name='generate_receipt'),
      path('send-message/', views.send_message, name='send_message'),  # Add this line
    
]