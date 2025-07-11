# Multi-stage build for optimized production image
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install ALL dependencies (including dev dependencies for build)
RUN npm ci && npm cache clean --force

# Copy source code
COPY . .

# Build React app
RUN npm run build

# Production stage
FROM node:18-alpine AS runtime

# Install dumb-init and Python for Gemini tracker
RUN apk add --no-cache dumb-init python3 py3-pip

# Create app user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodeuser -u 1001

# Set working directory
WORKDIR /app

# Copy package files and install production dependencies only
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Copy built application from builder stage
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/server.js ./
COPY --from=builder /app/gemini_tracker.py ./
COPY --from=builder /app/gemini_tracker_cached.py ./
COPY --from=builder /app/gemini_deep_dive_cached.py ./
COPY --from=builder /app/config.py ./
COPY --from=builder /app/requirements.txt ./

# Install Python dependencies (override externally-managed-environment protection)
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

# Change ownership to nodeuser
RUN chown -R nodeuser:nodejs /app
USER nodeuser

# Expose port (Cloud Run will set PORT env var)
EXPOSE $PORT

# Health check removed for Railway compatibility

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start the application
CMD ["node", "server.js"]
