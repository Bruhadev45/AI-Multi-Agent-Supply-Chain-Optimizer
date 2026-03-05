# Multi-stage Dockerfile for AI Multi-Agent Supply Chain Optimizer
# Optimized for Hugging Face Spaces deployment

# ============ Stage 1: Build Frontend ============
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies (including devDependencies needed for build)
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Remove any .env files that could override the Docker ENV during build
RUN rm -f .env .env.local .env.production .env.development

# Set production environment — empty NEXT_PUBLIC_API_URL forces relative URLs
# so requests go through Next.js rewrites to the backend on localhost:8000
ENV NODE_ENV=production
ENV NEXT_PUBLIC_API_URL=''

# Build Next.js app
RUN npm run build

# ============ Stage 2: Python Backend + Frontend Runtime ============
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies and Node.js 20 from NodeSource
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    make \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
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

# Create startup script with proper health-check wait
COPY <<'EOF' /app/start.sh
#!/bin/bash

echo "Starting AI Multi-Agent Supply Chain Optimizer..."

# Start backend in background
cd /app/backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to actually respond (up to 60 seconds)
echo "Waiting for backend to become healthy..."
for i in $(seq 1 60); do
  if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend is healthy after ${i}s"
    break
  fi
  if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "ERROR: Backend process crashed during startup"
    exit 1
  fi
  sleep 1
done

if ! curl -sf http://localhost:8000/health > /dev/null 2>&1; then
  echo "WARNING: Backend not healthy after 60s, starting frontend anyway..."
fi

# Start frontend
cd /app/frontend
NODE_ENV=production npx next start --port 7860 --hostname 0.0.0.0 &
FRONTEND_PID=$!

echo "Services started!"
echo "  Backend PID: $BACKEND_PID (port 8000)"
echo "  Frontend PID: $FRONTEND_PID (port 7860)"

# Keep running until a process exits
wait -n
EXIT_CODE=$?
echo "A process exited with code $EXIT_CODE"
exit $EXIT_CODE
EOF

RUN chmod +x /app/start.sh

# Set working directory
WORKDIR /app

# Expose port 7860 (Hugging Face Spaces standard)
EXPOSE 7860

# Health check - give enough time for both services to start
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
  CMD curl -f http://localhost:7860/ || exit 1

# Start services
CMD ["/app/start.sh"]
