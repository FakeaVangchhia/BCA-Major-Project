from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=100)
    room_description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_booked = models.BooleanField(default=False)
    image = models.ImageField(upload_to='static/room_images/')

    def __str__(self):
        return self.room_number


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.guest}'s reservation for Room {self.room.room_number}"



class TableReservation(models.Model):
    TABLE_NUMBER_CHOICES = (
        ('1', 'Table 1'),
        ('2', 'Table 2'),
        ('3', 'Table 3'),
        ('4', 'Table 4'),
        ('5', 'Table 5'),
        ('6', 'Table 6'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    reserve_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    guest = models.IntegerField()
    table_number = models.CharField(max_length=2, choices=TABLE_NUMBER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.reserve_date}"


    



