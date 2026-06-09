from rest_framework import serializers
from .models import (
    User, KYCDocument, Vehicle, ChargerListing, ChargerPhoto,
    AvailabilitySchedule, AvailabilityBlock, Booking, SessionLog,
    Review, Message, Dispute, Transaction
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'name', 'photo_url', 'role', 'kyc_status', 'kyc_verified_at', 'is_banned', 'created_at')
        read_only_fields = ('kyc_status', 'kyc_verified_at', 'is_banned', 'created_at')

class KYCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDocument
        fields = '__all__'
        read_only_fields = ('status', 'rejection_reason', 'reviewed_by', 'reviewed_at', 'created_at')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('driver', 'created_at')

class ChargerPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargerPhoto
        fields = ('id', 'url', 'order_index')

class AvailabilityScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilitySchedule
        fields = '__all__'

class AvailabilityBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailabilityBlock
        fields = '__all__'

class ChargerListingSerializer(serializers.ModelSerializer):
    photos = ChargerPhotoSerializer(many=True, read_only=True)
    schedules = AvailabilityScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = ChargerListing
        fields = '__all__'
        read_only_fields = ('host', 'status', 'created_at')

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('driver', 'status', 'qr_token', 'created_at')

class SessionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionLog
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('reviewer', 'reviewer_role', 'created_at')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'sent_at', 'read_at')

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'
        read_only_fields = ('status', 'resolution', 'resolved_by', 'resolved_at', 'refund_amount')

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
