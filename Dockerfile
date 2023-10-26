# Python resmi imajını kullanma
FROM python:3.9-slim

# Çalışma dizinini belirleme
WORKDIR /app

# Bağımlılıkları kopyalama ve kurma
COPY requirements.txt .
RUN pip install python-multipart
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyalama
COPY ./app /app

# Uygulamayı çalıştırma
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
