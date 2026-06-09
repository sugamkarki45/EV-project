from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("The Phone number must be set")
        user = self.model(phone=phone, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, blank=True)
    photo_url = models.URLField(blank=True)
    role = models.JSONField(default=list) # ['driver', 'host']
    kyc_status = models.CharField(max_length=20, default='pending') # pending, verified, rejected
    kyc_verified_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

class KYCDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    id_type = models.CharField(max_length=20) # citizenship, passport
    front_url = models.URLField()
    back_url = models.URLField(null=True, blank=True)
    selfie_url = models.URLField()
    status = models.CharField(max_length=20, default='pending')
    rejection_reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_kycs')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Vehicle(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    plate_number = models.CharField(max_length=20)
    connector_types = models.JSONField(default=list) # ['CCS2', 'Type 2 AC']
    bluebook_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChargerListing(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='charger_listings')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending') # pending, active, paused, deactivated
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    address_full = models.TextField()
    address_display = models.CharField(max_length=255) # fuzzy address
    connector_types = models.JSONField(default=list)
    power_kw = models.DecimalField(max_digits=5, decimal_places=2)
    charger_level = models.CharField(max_length=20) # Level 1, Level 2, DC Fast
    pricing_model = models.CharField(max_length=20) # time, kwh, flat
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_kwh = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_flat = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_duration_mins = models.PositiveIntegerField(default=60)
    max_duration_mins = models.PositiveIntegerField(default=240)
    instant_book = models.BooleanField(default=False)
    min_trust_tier = models.PositiveIntegerField(default=1)
    amenity_tags = models.JSONField(default=list)
    access_instructions = models.TextField()
    house_rules = models.TextField()
    is_smart_charger = models.BooleanField(default=False)
    smart_charger_api_url = models.URLField(blank=True)
    smart_charger_api_key = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ChargerPhoto(models.Model):
    listing = models.ForeignKey(ChargerListing, on_delete=models.CASCADE, related_name='photos')
    url = models.URLField()
    order_index = models.PositiveIntegerField(default=0)

class AvailabilitySchedule(models.Model):
    listing = models.ForeignKey(ChargerListing, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.PositiveSmallIntegerField() # 0-6
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

class AvailabilityBlock(models.Model):
    listing = models.ForeignKey(ChargerListing, on_delete=models.CASCADE, related_name='blocks')
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)

class Booking(models.Model):
    listing = models.ForeignKey(ChargerListing, on_delete=models.CASCADE, related_name='bookings')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending_approval')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_mins = models.PositiveIntegerField()
    pricing_model = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    total_charged = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_hold_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_released_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    payment_reference = models.CharField(max_length=100, blank=True)
    escrow_released_at = models.DateTimeField(null=True, blank=True)
    qr_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    session_started_at = models.DateTimeField(null=True, blank=True)
    session_ended_at = models.DateTimeField(null=True, blank=True)
    kwh_delivered = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SessionLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='logs')
    event_type = models.CharField(max_length=50)
    event_data = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews')
    reviewer_role = models.CharField(max_length=10) # driver, host
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

class Dispute(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='disputes')
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    description = models.TextField()
    evidence_urls = models.JSONField(default=list)
    status = models.CharField(max_length=20, default='open') # open, resolved
    resolution = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='resolved_disputes')
    resolved_at = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=50) # booking_charge, host_payout, refund, etc.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    payment_gateway_ref = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class GuaranteeFundLedger(models.Model):
    type = models.CharField(max_length=10) # credit, debit
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    dispute = models.ForeignKey(Dispute, on_delete=models.SET_NULL, null=True)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class TrustTierHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tier_history')
    old_tier = models.PositiveSmallIntegerField()
    new_tier = models.PositiveSmallIntegerField()
    reason = models.CharField(max_length=255)
    changed_at = models.DateTimeField(auto_now_add=True)
