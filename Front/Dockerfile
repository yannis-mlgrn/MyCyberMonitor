# Étape 1: Build de l'application frontend
FROM node:22.15.0-slim AS builder

WORKDIR /app

# Copie les fichiers nécessaires
COPY package*.json ./
RUN npm install
COPY . .

# Utiliser une variable d'environnement dans le build
ARG VITE_API_URL=http://localhost:8000
RUN echo "VITE_API_URL=$VITE_API_URL" && npm run build

# Étape 2: Servir l'application avec Nginx
FROM nginx:alpine

# Copier les fichiers construits depuis l'étape précédente
COPY --from=builder /app/dist /usr/share/nginx/html

# Configurer Nginx pour servir l'application
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
