from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, VehicleViewSet, ChargerListingViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'listings', ChargerListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]
