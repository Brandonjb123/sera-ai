from models import Base, WidgetClient, SessionLocal, engine

# Buat tabel (termasuk kolom baru jika belum ada)
Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    # Hanya tambahkan data jika client "sera-demo" belum ada
    existing = db.query(WidgetClient).filter(WidgetClient.client_id == "sera-demo").first()
    if not existing:
        client = WidgetClient(
            client_id="sera-demo",
            allowed_domain="sera-ai-two.vercel.app",
            status="active",
            llm_provider="groq",
            llm_api_key=""  # Kosong dulu, nanti diisi lewat admin panel
        )
        db.add(client)
        db.commit()
        print("✅ Data dummy 'sera-demo' berhasil ditambahkan")
    else:
        print("✅ Data 'sera-demo' sudah ada, tidak perlu ditambahkan")
finally:
    db.close()