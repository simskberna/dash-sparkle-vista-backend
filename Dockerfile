FROM python:3.11-slim

WORKDIR /app

# SQLite için gerekli paketler
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# SQLite database'i oluştur
RUN python -c "from app.database import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]