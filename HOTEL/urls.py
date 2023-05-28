from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'HOTEL'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('menu', views.menu, name='menu'),
    path('gallery', views.gallery, name='gallery'),
    path('contact', views.contact, name='contact'),
    path('search_room', views.search_rooms, name='search-room'),
    path('reserve_room/<int:room_number>/', views.reserve_room, name='reserve-room'),
    path('booking_successful/<int:reservation_id>/', views.success, name='success'),

    # May
    path('payment/', views.payment, name='payment'),
    # path('success', views.payment_success, name='payment-success'),
    path('success' , views.success , name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('room_canceled/<int:reservation_id>/', views.room_canceled, name='cancel-reservation'),
    path('cancel_success', views.cancel_success, name='cancel-success'),
    path('add_room', views.add_room, name='add-room'),
    path('contact_view', views.contact_view, name='contact'),
    
    # Table Reservation
    path('table_reservation', views.table_reservation, name='table-reservation'),
    path('reservation_confirmation', views.table_confirm, name='reservation-confirmation'),
    path('table_cancel/<int:tablereservation_id>', views.cancel_table, name='table-cancel'),

    # Authentications
    path('accounts/login/', auth_views.LoginView.as_view(template_name='authentication/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile')
]
