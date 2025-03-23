from django.contrib import admin
from .models import Amenity, Room, Booking, Payment,Receipt, ChatMessage


# Register the Amenity model
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Amenity, AmenityAdmin)


# Register the Room model
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'price_per_night', 'capacity', 'available', 'is_booked')
    list_filter = ('room_type', 'available', 'is_booked')
    search_fields = ('room_type',)
    filter_horizontal = ('amenities',)  # For ManyToManyField for amenities

admin.site.register(Room, RoomAdmin)


# Register the Booking model
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in_date', 'check_out_date', 'number_of_guests', 'total_price', 'created_at')
    list_filter = ('check_in_date', 'check_out_date', 'created_at')
    search_fields = ('user_username', 'room_room_type')

admin.site.register(Booking, BookingAdmin)


# Register the Payment model
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'payment_status', 'payment_date', 'payment_reference')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('payment_reference', 'booking__id')

admin.site.register(Payment, PaymentAdmin)

# Register the Receipt model
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'amount', 'issued_at')
    list_filter = ('issued_at',)
    search_fields = ('user_username', 'booking_id')

admin.site.register(Receipt, ReceiptAdmin)


# Register the ChatMessage model
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'admin_message', 'user_message')
    list_filter = ('created_at',)
    search_fields = ('user__username',)

admin.site.register(ChatMessage, ChatMessageAdmin)

# admin.py

from django.contrib import admin
from .models import Message  # Import the Message model

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'is_read')  # Fields to display in list view
    list_filter = ('is_read', 'timestamp', 'sender', 'receiver')  # Add filters for easier searching
    search_fields = ('content', 'sender__username', 'receiver__username')  # Enable search by content, sender or receiver
    ordering = ('-timestamp',)  # Default ordering by the timestamp (latest first)

admin.site.register(Message, MessageAdmin)  # Register the Message model with custom admin
