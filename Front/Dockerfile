# Step 1: Build the frontend application
FROM node:22.15.0-slim AS builder

WORKDIR /app

# Copy the necessary files
COPY package*.json ./
RUN npm install
COPY . .

# Use an environment variable during the build
ARG VITE_API_URL=http://localhost:8000
RUN echo "VITE_API_URL=$VITE_API_URL" && npm run build

# Step 2: Serve the application with Nginx
FROM nginx:alpine

# Copy the built files from the previous step
COPY --from=builder /app/dist /usr/share/nginx/html

# Configure Nginx to serve the application
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
