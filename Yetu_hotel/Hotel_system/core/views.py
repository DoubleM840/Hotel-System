from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ChatMessage, Room, Booking, Payment
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User  
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Booking
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from decimal import Decimal
from .models import Room, Booking, Payment
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db import models
from django.shortcuts import render
from .models import Message, Booking


# Home view
def home(request):
    return render(request, 'home.html')


# Signup view
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        
        messages.success(request, "Signup successful! Please login.")
        return redirect('login')
    return render(request, 'signup.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('rooms')
        else:
            messages.error(request, "Invalid credentials! Please try again.")
    return render(request, 'login.html')


# View available rooms
@login_required(login_url='user_login') 
def available_rooms(request):
    rooms = Room.objects.filter(available=True)
    return render(request, 'available_rooms.html', {'rooms': rooms})

# View room details
def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)  # Fetch room by ID or return 404 if not found
    return render(request, 'room_details.html', {'room': room})

# Book a room
@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if room.is_booked:
        messages.error(request, 'This room is already booked. Please choose another room.')
        return redirect('rooms')  # Redirect to the rooms page

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        number_of_guests = request.POST.get('number_of_guests')

        nights = (datetime.strptime(check_out_date, '%Y-%m-%d') - datetime.strptime(check_in_date, '%Y-%m-%d')).days
        total_price = room.price_per_night * nights if nights > 0 else 0

        check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()

        booking = Booking(
            room=room,
            user=request.user,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests,
            total_price=total_price
        )
        booking.save()

        room.is_booked = True
        room.save()

        return redirect('booking_success')  # Redirect to a success page

    return render(request, 'book_room.html', {'room': room})

# Booking success page
def booking_success(request):
    latest_booking = Booking.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, 'booking_success.html', {'booking': latest_booking})


def payment_view(request, booking_id):
    # Get the booking details
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        # Get form data
        payment_method = request.POST.get('payment_method')
        payment_reference = request.POST.get('payment_reference')
        amount = booking.total_price  # Use the booking's total price as the amount

        # Validate form data
        if not payment_method or not payment_reference:
            return HttpResponse("All fields are required", status=400)

        # Create the Payment instance and save it to the database
        payment = Payment.objects.create(
            booking=booking,
            amount=Decimal(amount),
            payment_method=payment_method,
            payment_status='completed',  # Set status based on your logic
            payment_date=timezone.now(),
            payment_reference=payment_reference,
        )

        # Update the booking status if needed
        booking.status = 'paid'  # or another appropriate status
        booking.save()

        # Redirect to a success page or render a success message
        return redirect('payment_success', id=payment.id)

    # Render the payment form template on GET request
    return render(request, 'payment.html', {'booking': booking})


# Payment success view
class PaymentSuccessView(View):
    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, 'payment_success.html', {'payment': payment})


def payment_success(request, id):
    # Fetch the Payment object to display payment success details
    payment = get_object_or_404(Payment, id=id)
    return render(request, 'payment_success.html', {'payment': payment})



def dashboard(request):
    # Fetch all the bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    
    # Fetch messages for the logged-in user (either sent or received)
    messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
    
    # Optionally, you can further organize the messages by read/unread or timestamp
    unread_messages = messages.filter(is_read=False)  # Example: filtering unread messages
    
    # Calculate total revenue from bookings
    total_revenue = bookings.aggregate(total_revenue=models.Sum('total_price'))['total_revenue'] or 0
    
    return render(request, 'dashboard.html', {
        'bookings': bookings,
        'messages': messages,
        'unread_messages': unread_messages,
        'total_revenue': total_revenue,
    })



def generate_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Include all relevant room details in the context
    room = booking.room  # Get the related Room object
    
    # Render HTML template to string
    html = render_to_string('receipt.html', {'booking': booking, 'room': room})
    
    # Generate PDF from HTML
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.id}.pdf"'
    
    # Use pisa to generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # Check for errors during PDF generation
    if pisa_status.err:
        return HttpResponse('We had some errors generating your PDF', status=500)
    
    return response


def send_message(request):
    if request.method == 'POST':
        recipient_username = request.POST['recipient']
        content = request.POST['content']
        
        try:
            recipient = User.objects.get(username=recipient_username)
            message = Message.objects.create(
                sender=request.user,
                recipient=recipient,
                content=content
            )
            message.save()
            # Redirect back to dashboard or confirmation
            return redirect('dashboard')
        except User.DoesNotExist:
            # Handle case where recipient does not exist
            # You might show an error message on the dashboard
            pass
            
    return render(request, 'dashboard.html')

