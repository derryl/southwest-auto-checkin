from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from sw_checkin.forms import EmailForm, NameForm, ReservationForm
from sw_checkin.models import Passenger, Reservation


def index(request):
    return HttpResponse('Southwest checkin tool <a href="' + reverse('email') + '"> >>> </a>')


def email_view(request):
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        if email_form.is_valid():
            form_email = email_form.cleaned_data['email']
            passenger, created = Passenger.objects.get_or_create(email=form_email)
            return HttpResponseRedirect(reverse('passenger_name', args=[passenger.id]))

    else:
        email_form = EmailForm()

    return render(request, 'create-reservation.html', {
        'email_form': email_form,
        'name_form': NameForm(),
        'reservation_form': ReservationForm(),
        'state': 'email'
    })


def name_view(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)
    if request.method == 'POST':
        name_form = NameForm(request.POST)
        if name_form.is_valid():
            passenger.first_name = name_form.cleaned_data['first_name']
            passenger.last_name = name_form.cleaned_data['last_name']
            passenger.save()
            return HttpResponseRedirect(reverse('reservation', args=[passenger_id]))

    # GET -----
    name_form = NameForm(
        initial={
            'first_name': passenger.first_name,
            'last_name': passenger.last_name,
        }
    )

    return render(request, 'create-reservation.html', {
        'email_form': EmailForm(initial={'email': passenger.email}),
        'name_form': name_form,
        'reservation_form': ReservationForm(),
        'passenger': passenger,
        'state': 'name'
    })


def reservation_view(request, passenger_id):
    passenger = get_object_or_404(Passenger, id=passenger_id)

    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            confirmation_num = reservation_form.cleaned_data['confirmation_num']
            flight_date = reservation_form.cleaned_data['flight_date']
            flight_time = reservation_form.cleaned_data['flight_time']
            reservation = Reservation.objects.create(
                passenger=passenger,
                flight_date=flight_date,
                flight_time=flight_time,
                confirmation_num=confirmation_num
            )
            return HttpResponseRedirect(reverse('success', args=[reservation.id]))
    else:
        reservation_form = ReservationForm()

    name_form = NameForm(
        initial={
            'first_name': passenger.first_name,
            'last_name': passenger.last_name,
        }
    )

    return render(request, 'create-reservation.html', {
        'email_form': EmailForm(initial={'email': passenger.email}),
        'name_form': name_form,
        'reservation_form': reservation_form,
        'passenger': passenger,
        'state': 'reservation'
    })


def success_view(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return HttpResponse(reservation.__str__())

