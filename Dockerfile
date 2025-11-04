# Dockerfile for Shelf MCP Server
# Optimized for Smithery deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the MCP server
COPY shelf_mcp_server.py .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port (if needed for HTTP mode in future)
# EXPOSE 8000

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the MCP server
CMD ["python", "shelf_mcp_server.py"]
