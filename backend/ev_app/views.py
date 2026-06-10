from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import (
    User, KYCDocument, Vehicle, ChargerListing, Booking, Review, Message, Dispute
)
from .serializers import (
    UserSerializer, KYCDocumentSerializer, VehicleSerializer,
    ChargerListingSerializer, BookingSerializer, ReviewSerializer,
    MessageSerializer, DisputeSerializer
)

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='request-otp')
    def request_otp(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        # Simulation: In a real app, send SMS OTP here.
        return Response({"message": "OTP sent successfully (simulation)"})

    @action(detail=False, methods=['post'], url_path='verify-otp')
    def verify_otp(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')
        if not phone or not otp:
            return Response({"error": "Phone and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Simulation: Accept any 6-digit OTP
        if len(otp) == 6:
            user, created = User.objects.get_or_create(phone=phone)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    queryset = Vehicle.objects.all()

    def get_queryset(self):
        return self.queryset.filter(driver=self.request.user)

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

class ChargerListingViewSet(viewsets.ModelViewSet):
    serializer_class = ChargerListingSerializer
    queryset = ChargerListing.objects.all()
    filterset_fields = ['charger_level', 'pricing_model']

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return self.queryset.filter(status='active')
        return self.queryset.filter(host=self.request.user)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        return self.queryset.filter(driver=self.request.user) | self.queryset.filter(listing__host=self.request.user)

    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)

    @action(detail=True, methods=['post'], url_path='start-session')
    def start_session(self, request, pk=None):
        booking = self.get_object()
        # Simulation: verify QR/GPS here
        booking.status = 'in_progress'
        booking.session_started_at = timezone.now()
        booking.save()
        return Response(BookingSerializer(booking).data)

    @action(detail=True, methods=['post'], url_path='end-session')
    def end_session(self, request, pk=None):
        booking = self.get_object()
        booking.status = 'completed'
        booking.session_ended_at = timezone.now()
        booking.save()
        return Response(BookingSerializer(booking).data)
