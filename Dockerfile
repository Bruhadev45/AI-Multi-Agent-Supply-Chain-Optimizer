# Multi-stage Dockerfile for AI Multi-Agent Supply Chain Optimizer
# Optimized for Hugging Face Spaces deployment

# ============ Stage 1: Build Frontend ============
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source
COPY frontend/ ./

# Set production environment
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=/api

# Build Next.js app
RUN npm run build

# ============ Stage 2: Python Backend + Frontend Runtime ============
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    nodejs \
    npm \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/node_modules ./frontend/node_modules
COPY --from=frontend-builder /app/frontend/package.json ./frontend/
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY frontend/next.config.mjs ./frontend/

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "Starting AI Multi-Agent Supply Chain Optimizer..."\n\
\n\
# Start backend in background\n\
cd /app/backend\n\
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &\n\
BACKEND_PID=$!\n\
\n\
# Wait for backend to be ready\n\
echo "Waiting for backend to start..."\n\
sleep 5\n\
\n\
# Start frontend\n\
cd /app/frontend\n\
NODE_ENV=production npm start -- --port 7860 --hostname 0.0.0.0 &\n\
FRONTEND_PID=$!\n\
\n\
echo "Services started!"\n\
echo "Backend PID: $BACKEND_PID"\n\
echo "Frontend PID: $FRONTEND_PID"\n\
\n\
# Wait for any process to exit\n\
wait -n\n\
\n\
# Exit with status of process that exited first\n\
exit $?\n\
' > /app/start.sh

RUN chmod +x /app/start.sh

# Set working directory
WORKDIR /app

# Expose port 7860 (Hugging Face Spaces standard)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Start services
CMD ["/app/start.sh"]
