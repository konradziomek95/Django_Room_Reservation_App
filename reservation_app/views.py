from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from reservation_app.models import Room, Reservation
import datetime


# Create your views here.
class Homepage(View):
    def get(self, request):
        return render(request, 'homepage.html')


def check_input(value):
    validator = Room.objects.filter(name=value).first()
    if validator is not None:
        return True
    else:
        return False


@method_decorator(csrf_exempt, name='dispatch')
class NewRoom(View):
    def get(self, request):
        return render(request, 'add-room.html')

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector_available')
        error = None
        if projector is None:
            projector_available = False
        else:
            projector_available = True
        if not name or not capacity:
            error = "You can't leave empty fields"
            return render(request, 'add-room.html', {'error': error})
        if check_input(name) is True:
            error = "Conference room with that name is existing in DB"
            return render(request, 'add-room.html', {'error': error})
        Room.objects.create(name=name, capacity=capacity, projector=projector_available)
        return redirect('homepage')


class RoomList(View):
    def get(self, request):
        rooms = Room.objects.all()
        for room in rooms:
            reservation_today = Reservation.objects.filter(room_id=room.id).filter(date=datetime.date.today())
            if reservation_today:
                room.availability = True
        ctx = {
            'rooms': rooms,
        }
        return render(request, 'available-rooms.html', ctx)


@method_decorator(csrf_exempt, name='dispatch')
class DeleteRoom(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        warning = f'Do you really want to delete {room.name}?'
        ctx = {
            'room': room,
            'warning': warning,
        }
        return render(request, 'delete-room.html', ctx)

    def post(self, request, id):
        room = Room.objects.get(id=id)
        room.delete()
        return redirect('homepage')


@method_decorator(csrf_exempt, name='dispatch')
class ModifyRoom(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        ctx = {
            'room': room,
        }
        return render(request, 'modify-room.html', ctx)

    def post(self, request, id):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        projector = request.POST.get('projector_available')
        room = Room.objects.get(id=id)
        error = None
        if projector is None:
            projector_available = False
        else:
            projector_available = True
        if not name or not capacity:
            error = "You can't leave empty fields"
            return render(request, 'modify-room.html', {'room': room, 'error': error})

        if name != room.name and check_input(name) is True:
            error = "Conference room with that name is existing in DB"
            return render(request, 'modify-room.html', {'room': room, 'error': error})

        room.name = name
        room.capacity = capacity
        room.projector = projector_available
        room.save()
        return redirect('homepage')


@method_decorator(csrf_exempt, name='dispatch')
class NewReservation(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = Reservation.objects.filter(room_id=id, date__gte=datetime.date.today())
        return render(request, 'add-reservation.html', {'room': room, 'reservations': reservations})

    def post(self, request, id):
        room = Room.objects.get(id=id)
        date = request.POST.get('date')
        comment = request.POST.get('comment')
        error = str(date)
        if date < str(datetime.date.today()):
            error = 'You can,t reserve room in past time!'
            return render(request, 'add-reservation.html', {'room': room, 'error': error})

        if Reservation.objects.filter(room=room, date=date):
            error = f"In this date {room.name} is reserved!"
            return render(request, "add-reservation.html", {"room": room, "error": error})
        Reservation.objects.create(date=date, comment=comment, room_id=room.id)
        return redirect('homepage')


class RoomInfo(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = Reservation.objects.filter(room_id=id, date__gte=datetime.date.today())
        ctx = {
            'room': room,
            'reservations': reservations,
        }
        return render(request, 'room-info.html', ctx)
