# Utiliser une image officielle Python
FROM python:3.11-slim

WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# Copier le code
COPY app ./app

# Lancer Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
