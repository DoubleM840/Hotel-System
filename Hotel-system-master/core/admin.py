from django.contrib import admin
from .models import Amenity, Room, Booking, Payment, ChatMessage, Billing, Message

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'price_per_night', 'capacity', 'available', 'is_booked')
    list_filter = ('room_type', 'available', 'is_booked')
    search_fields = ('room_type', 'description')
    filter_horizontal = ('amenities',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in_date', 'check_out_date', 'total_price', 'created_at')
    list_filter = ('check_in_date', 'check_out_date', 'room__room_type')
    search_fields = ('user__username', 'room__room_type')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'payment_method', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_method')
    search_fields = ('booking__user__username', 'payment_reference')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'payment_date')
    list_filter = ('status',)
    search_fields = ('user__username',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_admin')
    list_filter = ('is_admin', 'created_at')
    search_fields = ('user__username', 'message')
