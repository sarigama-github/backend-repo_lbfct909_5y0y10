import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Teacher, Program, News, Event, AdmissionApplication, ContactMessage, Settings

app = FastAPI(title="SMA Modern School API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SMA Modern Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Basic content endpoints (list only for public site)
@app.get("/api/teachers", response_model=List[Teacher])
def list_teachers(limit: Optional[int] = None):
    docs = get_documents("teacher", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/programs", response_model=List[Program])
def list_programs(limit: Optional[int] = None):
    docs = get_documents("program", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/news", response_model=List[News])
def list_news(limit: Optional[int] = 10):
    docs = get_documents("news", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/api/events", response_model=List[Event])
def list_events(limit: Optional[int] = 10):
    docs = get_documents("event", {}, limit)
    for d in docs:
        d.pop("_id", None)
    return docs

# Public forms: admissions and contact
@app.post("/api/admissions")
def submit_admission(payload: AdmissionApplication):
    inserted_id = create_document("admissionapplication", payload)
    return {"status": "ok", "id": inserted_id}

@app.post("/api/contact")
def submit_contact(payload: ContactMessage):
    inserted_id = create_document("contactmessage", payload)
    return {"status": "ok", "id": inserted_id}

# Settings (single document). For demo, expose read; in real app protect write.
@app.get("/api/settings", response_model=List[Settings])
def get_settings():
    docs = get_documents("settings", {}, limit=1)
    for d in docs:
        d.pop("_id", None)
    return docs

# Optional: seeding endpoint to quickly populate sample content
@app.post("/api/seed")
def seed_sample_content():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not available")

    # Only seed if empty
    created = {"teachers": 0, "programs": 0, "news": 0, "events": 0, "settings": 0}

    if db["teacher"].count_documents({}) == 0:
        sample_teachers = [
            {"name": "Ahmad Fikri, S.Pd", "subject": "Matematika", "bio": "Pengajar berpengalaman Olimpiade Matematika.", "photo_url": "https://images.unsplash.com/photo-1600267175161-cfaa711b4a81?w=400"},
            {"name": "Dewi Lestari, M.Pd", "subject": "Bahasa Indonesia", "bio": "Aktif menulis dan pembina mading sekolah.", "photo_url": "https://images.unsplash.com/photo-1544006659-f0b21884ce1d?w=400"},
            {"name": "Rizky Pratama, M.Si", "subject": "Fisika", "bio": "Peneliti muda dan pembina klub robotik.", "photo_url": "https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=400"},
        ]
        for t in sample_teachers:
            create_document("teacher", t)
        created["teachers"] = len(sample_teachers)

    if db["program"].count_documents({}) == 0:
        sample_programs = [
            {"name": "MIPA", "description": "Fokus sains dan teknologi.", "icon": "flask-round", "level": "IPA"},
            {"name": "IPS", "description": "Fokus sosial dan ekonomi.", "icon": "library", "level": "IPS"},
            {"name": "Bahasa", "description": "Fokus bahasa dan budaya.", "icon": "book-open", "level": "BHS"},
        ]
        for p in sample_programs:
            create_document("program", p)
        created["programs"] = len(sample_programs)

    if db["news"].count_documents({}) == 0:
        sample_news = [
            {"title": "SMA Modern Juara Lomba Sains", "content": "Tim MIPA meraih juara umum pada kompetisi sains tingkat provinsi.", "image_url": "https://images.unsplash.com/photo-1551836022-4c4c79ecde51?w=800"},
            {"title": "Penerimaan Peserta Didik Baru Dibuka", "content": "Pendaftaran PPDB tahun ajaran baru telah resmi dibuka.", "image_url": "https://images.unsplash.com/photo-1555243896-c709bfa0b564?w=800"},
        ]
        for n in sample_news:
            create_document("news", n)
        created["news"] = len(sample_news)

    if db["event"].count_documents({}) == 0:
        sample_events = [
            {"title": "Open House & Campus Tour", "description": "Kunjungan fasilitas sekolah untuk calon siswa.", "date": datetime.utcnow(), "location": "Kampus SMA Modern"},
            {"title": "Tryout UTBK Gratis", "description": "Simulasi UTBK untuk kelas XII.", "date": datetime.utcnow(), "location": "Aula Utama"},
        ]
        for e in sample_events:
            create_document("event", e)
        created["events"] = len(sample_events)

    if db["settings"].count_documents({}) == 0:
        settings = {
            "school_name": "SMA Modern Nusantara",
            "tagline": "Sekolah unggulan dengan pendekatan modern",
            "address": "Jl. Pendidikan No. 123, Jakarta",
            "phone": "+62 812-3456-7890",
            "email": "info@smamodern.sch.id",
            "facebook": "https://facebook.com/smamodern",
            "instagram": "https://instagram.com/smamodern",
            "youtube": "https://youtube.com/@smamodern"
        }
        create_document("settings", settings)
        created["settings"] = 1

    return {"status": "ok", "created": created}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
