"""
Database Schemas for SMA Modern School Site

Each Pydantic model below corresponds to a MongoDB collection (collection name is the lowercase of the class name).
Use these models to validate incoming/outgoing data and to understand the data structure stored in the database.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

# Core content
class Teacher(BaseModel):
    name: str = Field(..., description="Full name of the teacher")
    subject: str = Field(..., description="Main subject taught")
    bio: Optional[str] = Field(None, description="Short biography")
    photo_url: Optional[HttpUrl] = Field(None, description="Profile photo URL")

class Program(BaseModel):
    name: str = Field(..., description="Program name (e.g., MIPA / IPS / Bahasa)")
    description: Optional[str] = Field(None, description="Program description")
    icon: Optional[str] = Field(None, description="Icon name for UI purposes")
    level: Optional[str] = Field(None, description="Education stream or specialization")

class News(BaseModel):
    title: str = Field(..., description="News title")
    content: str = Field(..., description="News content (markdown or plain text)")
    image_url: Optional[HttpUrl] = Field(None, description="Cover image URL")
    published_at: Optional[datetime] = Field(None, description="Publish datetime")

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    description: Optional[str] = Field(None, description="Event description")
    date: datetime = Field(..., description="Event date and time")
    location: Optional[str] = Field(None, description="Event location")

# Interactions
class AdmissionApplication(BaseModel):
    full_name: str = Field(..., description="Applicant's full name")
    email: str = Field(..., description="Applicant email")
    phone: str = Field(..., description="Applicant phone number")
    previous_school: Optional[str] = Field(None, description="Previous school")
    message: Optional[str] = Field(None, description="Additional message")

class ContactMessage(BaseModel):
    name: str = Field(..., description="Sender name")
    email: str = Field(..., description="Sender email")
    message: str = Field(..., description="Message content")

# Site settings
class Settings(BaseModel):
    school_name: str = Field(..., description="School name")
    tagline: Optional[str] = Field(None, description="Short tagline")
    address: Optional[str] = Field(None, description="School address")
    phone: Optional[str] = Field(None, description="Contact phone")
    email: Optional[str] = Field(None, description="Contact email")
    facebook: Optional[str] = Field(None, description="Facebook URL")
    instagram: Optional[str] = Field(None, description="Instagram URL")
    youtube: Optional[str] = Field(None, description="YouTube URL")
