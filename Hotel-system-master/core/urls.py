# myapp/urls.py

from django.urls import path
from .views import available_rooms,signup,login,dashboard,generate_receipt, cancel_booking,dashboard, room_details,home,cancel_booking, book_room, booking_success,process_payment,PaymentSuccessView

urlpatterns = [
    path('', home, name='home'),  # Assuming you have a home view
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('rooms/', available_rooms, name='rooms'),  # Add this line
    path('rooms/<int:room_id>/', room_details, name='room_details'),  # For room details
    path('book/<int:room_id>/', book_room, name='book_room'),  # URL for booking a room
    path('booking-success/', booking_success, name='booking_success'),  # URL for booking success
      path('payment/<int:booking_id>/', process_payment, name='process_payment'), 
      path('payment/success/<int:payment_id>/', PaymentSuccessView.as_view(), name='payment_success'),  # URL for payment success
      path('dashboard/', dashboard, name='dashboard'),
      path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'), 
    path('admin/cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('generate_receipt/<int:booking_id>/', generate_receipt, name='generate_receipt'),
]
