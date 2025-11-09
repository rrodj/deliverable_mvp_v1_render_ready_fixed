from __future__ import annotations
from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Numeric, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

def SessionLocal(db_url: str):
    engine = create_engine(db_url, future=True)
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"
    id = Column(String, primary_key=True)
    name = Column(Text, nullable=False)

    users = relationship("User", back_populates="org", cascade="all, delete-orphan")
    devices = relationship("Device", back_populates="org", cascade="all, delete-orphan")
    menu_uploads = relationship("MenuUpload", back_populates="org", cascade="all, delete-orphan")
    menu_items = relationship("MenuItem", back_populates="org", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="org", cascade="all, delete-orphan")

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    email = Column(Text, nullable=False, unique=True)
    name = Column(Text)
    password_hash = Column(Text)
    role = Column(String, default="admin", nullable=False)

    org = relationship("Organization", back_populates="users")

class Device(Base, TimestampMixin):
    __tablename__ = "devices"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(Text, nullable=False)
    device_type = Column(Text, nullable=False)

    org = relationship("Organization", back_populates="devices")
    calibrations = relationship("Calibration", back_populates="device", cascade="all, delete-orphan")

class Calibration(Base):
    __tablename__ = "calibrations"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    device_id = Column(String, ForeignKey("devices.id", ondelete="CASCADE"), nullable=False)
    offset = Column(Numeric(10,4), nullable=False)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(String, ForeignKey("users.id"))

    device = relationship("Device", back_populates="calibrations")
    org = relationship("Organization")
    creator = relationship("User")

    __table_args__ = (
        Index("idx_calibrations_device_created", "device_id", "created_at"),
    )

class MenuUpload(Base):
    __tablename__ = "menu_uploads"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    uploaded_by = Column(String, ForeignKey("users.id"))
    source_filename = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    org = relationship("Organization", back_populates="menu_uploads")
    items = relationship("MenuItem", back_populates="upload")

class MenuItem(Base, TimestampMixin):
    __tablename__ = "menu_items"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    upload_id = Column(String, ForeignKey("menu_uploads.id", ondelete="SET NULL"))
    sku = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    price = Column(Numeric(10,2))
    active = Column(Boolean, nullable=False, default=True)

    org = relationship("Organization", back_populates="menu_items")
    upload = relationship("MenuUpload", back_populates="items")

    __table_args__ = (
        Index("idx_menu_items_org_created", "org_id", "created_at"),
    )

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    type = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    acknowledged = Column(Boolean, default=False, nullable=False)
    acknowledged_at = Column(DateTime)
    acknowledged_by = Column(String, ForeignKey("users.id"))

    org = relationship("Organization", back_populates="alerts")
    __table_args__ = (
        CheckConstraint("level in ('info','warning','critical')", name="ck_alert_level"),
        Index("idx_alerts_org_created", "org_id", "created_at"),
    )

class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("organizations.id", ondelete="SET NULL"))
    provider = Column(Text, nullable=False)
    event_type = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    payload_json = Column(Text)

    __table_args__ = (
        Index("idx_webhook_provider_time", "provider", "received_at"),
    )
