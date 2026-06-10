from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime, JSON, ForeignKey, DECIMAL, Integer, Time, Text, UUID
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
from datetime import datetime, time
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), default="")
    photo_url: Mapped[Optional[str]] = mapped_column(String(512))
    roles: Mapped[List[str]] = mapped_column(JSON, default=list) # driver, home_owner, hotel_owner, airbnb_host
    kyc_status: Mapped[str] = mapped_column(String(20), default="pending") # pending, verified, rejected
    kyc_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    trust_tier: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    vehicles = relationship("Vehicle", back_populates="driver")
    listings = relationship("ChargerListing", back_populates="host")
    bookings = relationship("Booking", back_populates="driver", foreign_keys="Booking.driver_id")
    wallet = relationship("Wallet", back_populates="user", uselist=False)

class KYCDocument(Base):
    __tablename__ = "kyc_documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    id_type: Mapped[str] = mapped_column(String(20)) # citizenship, passport
    front_url: Mapped[str] = mapped_column(String(512))
    back_url: Mapped[Optional[str]] = mapped_column(String(512))
    selfie_url: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(20), default="pending")
    rejection_reason: Mapped[str] = mapped_column(Text, default="")
    reviewed_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"))
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    make: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    plate_number: Mapped[str] = mapped_column(String(20))
    connector_types: Mapped[List[str]] = mapped_column(JSON, default=list)
    bluebook_url: Mapped[str] = mapped_column(String(512))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    driver = relationship("User", back_populates="vehicles")

class ChargerListing(Base):
    __tablename__ = "charger_listings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    host_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    host_type: Mapped[str] = mapped_column(String(20)) # home, hotel_restaurant, airbnb
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    geo_location = mapped_column(Geography(geometry_type='POINT', srid=4326))
    address_full: Mapped[str] = mapped_column(Text)
    address_display: Mapped[str] = mapped_column(String(255))
    connector_types: Mapped[List[str]] = mapped_column(JSON, default=list)
    power_kw: Mapped[float] = mapped_column(DECIMAL(5, 2))
    charger_level: Mapped[str] = mapped_column(String(20))
    pricing_model: Mapped[str] = mapped_column(String(20)) # hourly, kwh, flat
    price_per_hour: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2))
    price_per_kwh: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2))
    price_flat: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 2))
    min_duration_mins: Mapped[int] = mapped_column(Integer, default=60)
    max_duration_mins: Mapped[int] = mapped_column(Integer, default=240)
    instant_book: Mapped[bool] = mapped_column(Boolean, default=False)
    min_trust_tier: Mapped[int] = mapped_column(Integer, default=1)
    amenity_tags: Mapped[List[str]] = mapped_column(JSON, default=list)
    access_instructions: Mapped[str] = mapped_column(Text)
    house_rules: Mapped[str] = mapped_column(Text)
    is_smart_charger: Mapped[bool] = mapped_column(Boolean, default=False)
    smart_charger_api_url: Mapped[Optional[str]] = mapped_column(String(512))
    smart_charger_api_key: Mapped[Optional[str]] = mapped_column(String(255))
    business_registration_url: Mapped[Optional[str]] = mapped_column(String(512))
    property_url: Mapped[Optional[str]] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    host = relationship("User", back_populates="listings")
    photos = relationship("ChargerPhoto", back_populates="listing")
    schedules = relationship("AvailabilitySchedule", back_populates="listing")
    bookings = relationship("Booking", back_populates="listing")

class ChargerPhoto(Base):
    __tablename__ = "charger_photos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("charger_listings.id"))
    url: Mapped[str] = mapped_column(String(512))
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    listing = relationship("ChargerListing", back_populates="photos")

class AvailabilitySchedule(Base):
    __tablename__ = "availability_schedules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("charger_listings.id"))
    day_of_week: Mapped[int] = mapped_column(Integer) # 0-6
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    listing = relationship("ChargerListing", back_populates="schedules")

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("charger_listings.id"))
    driver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    vehicle_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("vehicles.id"))
    status: Mapped[str] = mapped_column(String(20), default="pending_approval")
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    duration_mins: Mapped[int] = mapped_column(Integer)
    pricing_model: Mapped[str] = mapped_column(String(20))
    rate: Mapped[float] = mapped_column(DECIMAL(10, 2))
    subtotal: Mapped[float] = mapped_column(DECIMAL(10, 2))
    platform_fee: Mapped[float] = mapped_column(DECIMAL(10, 2))
    total_charged: Mapped[float] = mapped_column(DECIMAL(10, 2))
    deposit_hold_amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    deposit_released_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    payment_method: Mapped[str] = mapped_column(String(50))
    payment_reference: Mapped[Optional[str]] = mapped_column(String(100))
    escrow_released_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    qr_token: Mapped[str] = mapped_column(String(255), unique=True, default=lambda: str(uuid.uuid4()))
    session_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    session_ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    kwh_delivered: Mapped[Optional[float]] = mapped_column(DECIMAL(7, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    listing = relationship("ChargerListing", back_populates="bookings")
    driver = relationship("User", back_populates="bookings", foreign_keys=[driver_id])
    logs = relationship("SessionLog", back_populates="booking")

class AvailabilityBlock(Base):
    __tablename__ = "availability_blocks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("charger_listings.id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    reason: Mapped[str] = mapped_column(String(255), default="")

class SessionLog(Base):
    __tablename__ = "session_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"))
    event_type: Mapped[str] = mapped_column(String(50))
    event_data: Mapped[dict] = mapped_column(JSON, default=dict)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    booking = relationship("Booking", back_populates="logs")

class Review(Base):
    __tablename__ = "reviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"), unique=True)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    reviewee_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    reviewer_role: Mapped[str] = mapped_column(String(10)) # driver, host
    rating: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"))
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

class Dispute(Base):
    __tablename__ = "disputes"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("bookings.id"))
    raised_by_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    reason: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    evidence_urls: Mapped[List[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(20), default="open")
    resolution: Mapped[str] = mapped_column(Text, default="")
    resolved_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id"))
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    refund_amount: Mapped[float] = mapped_column(DECIMAL(10, 2), default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    type: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    reference_booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("bookings.id"))
    payment_gateway_ref: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class GuaranteeFundLedger(Base):
    __tablename__ = "guarantee_fund_ledger"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(10)) # credit, debit
    amount: Mapped[float] = mapped_column(DECIMAL(10, 2))
    booking_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("bookings.id"))
    dispute_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("disputes.id"))
    balance_after: Mapped[float] = mapped_column(DECIMAL(15, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class TrustTierHistory(Base):
    __tablename__ = "trust_tier_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    old_tier: Mapped[int] = mapped_column(Integer)
    new_tier: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(String(255))
    changed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Wallet(Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True)
    balance_npr: Mapped[float] = mapped_column(DECIMAL(15, 2), default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="wallet")
