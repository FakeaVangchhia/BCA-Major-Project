from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from .models import Room, Reservation, Guest, TableReservation
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404


from django.contrib import messages
from .models import TableReservation

# Contact
from .forms import ContactForm

# auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout


def index(request):
    return render(request, 'hotel/index.html', {})


def about(request):
    return render(request, 'hotel/about.html', {})


def menu(request):
    return render(request, 'hotel/menu.html', {})


def contact(request):
    return render(request, 'hotel/contact.html', {})


def gallery(request):
    return render(request, 'hotel/gallery.html', {})


@login_required
def search_rooms(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    available_rooms = Room.objects.filter(is_booked=False)
    if start_date and end_date:
        # Find reservations that overlap with the requested dates
        reservations = Reservation.objects.filter(
            Q(start_date__range=[start_date, end_date]) | Q(end_date__range=[start_date, end_date])
        )
        booked_rooms = [reservation.room for reservation in reservations]
        available_rooms = available_rooms.exclude(pk__in=[room.pk for room in booked_rooms])
    context = {'available_rooms_list': available_rooms, 'start_date': start_date, 'end_date': end_date}
    return render(request, 'booking/room_search.html', context)



@login_required
def add_room(request):
    if request.method == 'POST':
        room = Room(
            room_number=request.POST.get('room_number'),
            room_type=request.POST.get('room_type'),
            room_description=request.POST.get('room_description'),
            price=request.POST.get('price'),
            is_booked=request.POST.get('is_booked'),
            image=request.FILES.get('image')
        )
        room.save()
        context = {
            'room_number': room.room_number
        }
        return render(request, 'booking/room_added.html', context)
    else:
        return render(request, 'booking/add_room.html')



# function for the reserve room and making payment.
@csrf_exempt
@login_required
def reserve_room(request, **kwargs):
    room_number = kwargs['room_number']
    room = Room.objects.get(room_number=room_number)
    price = room.price
    user = request.user

    if request.method == 'POST':
        # Check if a guest object already exists for the user
        guest, created = Guest.objects.get_or_create(user=user)

        # Update the fields of the existing guest object using the form data
        guest.first_name = request.POST['first_name']
        guest.last_name = request.POST['last_name']
        guest.email = request.POST['email']
        guest.phone_number = request.POST['phone_number']
        guest.save()

        # Create a new Reservation object using the form data and the Guest object
        reservation = Reservation.objects.create(
            room=Room.objects.get(room_number=request.POST['room_number']),
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            guest=guest
        )
        # Render the reservation_confirm template after payment successful
        return render(request, 'booking/success.html', {'reservation': reservation})
    else:
        # Render the form for the user to fill out
        return render(request, 'booking/reserve_room.html', {
            'room_number': room_number,
            'price': price * 100,
        })



@csrf_exempt
def booking_success(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    print(reservation)
    context = {'reservation': reservation}
    return render(request, 'booking/success.html', context)



def room_canceled(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    return redirect('HOTEL:cancel-success')




def cancel_success(request):
    return render(request, 'booking/room_canceled.html')   


def payment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 50000

        client = razorpay.Client(
            auth=("rzp_test_N94crIsOHAqIqA", "mO0T0vP3J6wajyEV6UDDztoG"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'booking/payment.html')

@csrf_exempt
def success(request):
    return render(request, "booking/success.html")


@csrf_exempt
def success(request, reservation_id):
    reservation = Reservation.objects.all(id=reservation_id)
    context = {'reservation': reservation}
    return render(request, 'booking/success.html', context)


@login_required
def dashboard(request):
    user = request.user
    
    if user.is_staff:
        # User is a manager - show all reservations
        reservations = Reservation.objects.all()
        tables = TableReservation.objects.all
        guests = Guest.objects.all()
    else:
        # User is a guest - show only their own reservations
        reservations = Reservation.objects.filter(guest__user=user)
        tables = TableReservation.objects.filter(user=user)
        guests = Guest.objects.filter(reservation__guest__user=request.user)

    
    return render(request, 'booking/dashboard.html', {
        'user': user,
        'reservations': reservations,
        'tables': tables, 
        'guests': guests
        })



# authentications
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('HOTEL:profile')
    else:
        form = UserCreationForm()
    return render(request, 'authentication/signup.html', {
        'form': form
    })


def custom_logout(request):
    logout(request)
    return redirect('HOTEL:index')

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'authentication/profile.html', context)



@login_required
def table_reservation(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        reserve_date = request.POST['reserve_date']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        guest = request.POST['guest']
        table_number = request.POST['table_number']

        # Check if table is available for reservation
        reservations = TableReservation.objects.filter(
            table_number=table_number,
            reserve_date=reserve_date,
            start_time__lte=end_time,
            end_time__gte=start_time,
        )

        if reservations.exists():
            messages.error(request, 'This table is not available for the selected date and time. Please choose another table or time.')
            return redirect('HOTEL:table-reservation')

        # Create a new reservation
        user = request.user
        reservation = TableReservation(
            user=user,
            first_name=first_name,
            last_name=last_name,
            reserve_date=reserve_date,
            start_time=start_time,
            guest=guest,
            end_time=end_time,

            table_number=table_number,
        )
        reservation.save()
        return redirect('HOTEL:reservation-confirmation')

    else:
        tables = TableReservation.TABLE_NUMBER_CHOICES
        context = {
            'table_choices': tables
        }
        return render(request, 'table/reservation.html', context)


    
def table_confirm(request):
    table = TableReservation.objects.filter(user=request.user).latest('id')
    
    table_number = table.table_number
    time = table.start_time
    return render(request, 'table/reservation_confimation.html', {
        'table_number': table_number,
        'time': time
    })

def cancel_table(request, tablereservation_id):
    table = get_object_or_404(TableReservation, id=tablereservation_id)
    table.delete()
    return redirect('HOTEL:cancel-success')


# contact page
@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            return render(request, 'authentication/email_sent.html')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'recipient_email': 'fakeavangchhia@.com', # replace with your email address
    }
    return render(request, 'hotel/contact.html', context)



