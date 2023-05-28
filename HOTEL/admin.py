from django.contrib import admin
from .models import Reservation, Room, Guest, TableReservation

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Guest)
admin.site.register(TableReservation)

