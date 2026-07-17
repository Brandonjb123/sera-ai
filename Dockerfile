# Gunakan image Python 3.11 yang ringan
FROM python:3.11-slim

# Atur working directory
WORKDIR /app

RUN mkdir -p /app/data

# Salin dan install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode proyek
COPY . .

# Pindah ke folder backend untuk menjalankan aplikasi
WORKDIR /app/backend

# Jalankan aplikasi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]