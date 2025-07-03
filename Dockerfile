# Use a specific, lightweight Python version
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install the `websockets` library, which is the only dependency for the server
RUN pip install websockets

# --- Security Best Practice ---
# Create a dedicated, non-root user to run the application
RUN useradd -m demo
USER demo

# Expose the port the WebSocket server will run on
EXPOSE 8765

# The command to run when the container starts
CMD ["python", "-u", "websocket_server.py"]
