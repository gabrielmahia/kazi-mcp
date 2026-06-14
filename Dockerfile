# AI-KungFU East Africa MCP Server
# Glama-compatible Dockerfile for kazi-mcp
FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/gabrielmahia/kazi-mcp"
LABEL org.opencontainers.image.description="kazi-mcp — East Africa AI Coordination Infrastructure"
LABEL org.opencontainers.image.licenses="MIT"

RUN pip install --no-cache-dir kazi-mcp

CMD ["kazi-mcp"]
