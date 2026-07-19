from models import Base, WidgetClient, SessionLocal, engine

# Buat tabel
Base.metadata.create_all(bind=engine)

# Tambahkan data dummy
db = SessionLocal()
try:
    # Hapus data lama jika ada
    db.query(WidgetClient).delete()
    
    client = WidgetClient(
        client_id="sera-demo",
        allowed_domain="sera-ai-two.vercel.app",
        status="active"
    )
    db.add(client)
    db.commit()
    print("✅ Data dummy berhasil ditambahkan")
finally:
    db.close()