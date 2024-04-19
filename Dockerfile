# Stage 1: Build frontend
FROM node:latest AS frontend

# Set working directory for frontend
WORKDIR /app/frontend

# Copy frontend source code
COPY frontend/package.json frontend/package-lock.json ./
COPY frontend .

# Install dependencies
RUN npm install

# Build frontend
RUN npm run build

# Stage 2: Build backend
FROM python:3.9-slim AS backend

# Set working directory for backend
WORKDIR /app/backend

# Copy backend source code
COPY backend .

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Serve frontend and backend using nginx and gunicorn
FROM nginx:latest AS production

# Copy built frontend files from the frontend stage to nginx
COPY --from=frontend /app/frontend/dist /usr/share/nginx/html

# Copy built backend code from the backend stage
COPY --from=backend /app/backend /app/backend

# Expose port 80 for nginx
EXPOSE 80

# Start gunicorn server for backend
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

