from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def _str_(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = [
        ('deluxe', 'Deluxe Room'),
        ('executive', 'Executive Suite'),
        ('standard', 'Standard Room'),
    ]

    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_images/')
    capacity = models.PositiveIntegerField(help_text="Maximum number of guests")
    available = models.BooleanField(default=True)
    is_booked = models.BooleanField(default=False)
    amenities = models.ManyToManyField(Amenity, blank=True)

    def _str_(self):
        return f"{self.get_room_type_display()} - KSh {self.price_per_night}/night"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        nights = (self.check_out_date - self.check_in_date).days
        if nights > 0:
            self.total_price = self.room.price_per_night * nights
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Booking: {self.user.username} - {self.room.get_room_type_display()} from {self.check_in_date} to {self.check_out_date}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    payment_date = models.DateTimeField(default=timezone.now)
    payment_reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'Payment {self.id} for Booking {self.booking.id} - Status: {self.payment_status}'



class Receipt(models.Model):  # This class should be outside the Billing class
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Receipt for {self.user.username}"


class ChatMessage(models.Model):  # This class should be outside the Billing class
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    admin_message = models.TextField()
    user_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Chat with {self.user.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"



        