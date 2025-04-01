FROM python:3.10.4-slim-buster

# Update and install required OS packages
RUN apt update && apt upgrade -y && \
    apt-get install -y git curl python3-pip ffmpeg wget bash neofetch software-properties-common supervisor

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install wheel && pip3 install --no-cache-dir -U -r requirements.txt

# Ensure Flask is installed (if not already in requirements.txt)
RUN pip3 install flask

# Set working directory and copy the application code
WORKDIR /app
COPY . .

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor
RUN echo '[supervisord]' > /etc/supervisor/conf.d/app.conf && \
    echo 'nodaemon=true' >> /etc/supervisor/conf.d/app.conf && \
    echo '' >> /etc/supervisor/conf.d/app.conf && \
    echo '[program:flask]' >> /etc/supervisor/conf.d/app.conf && \
    echo 'command=python3 app.py' >> /etc/supervisor/conf.d/app.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/app.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/app.conf && \
    echo 'stderr_logfile=/var/log/supervisor/flask-err.log' >> /etc/supervisor/conf.d/app.conf && \
    echo 'stdout_logfile=/var/log/supervisor/flask-out.log' >> /etc/supervisor/conf.d/app.conf && \
    echo '' >> /etc/supervisor/conf.d/app.conf && \
    echo '[program:telegrambot]' >> /etc/supervisor/conf.d/app.conf && \
    echo 'command=python3 -m Restriction' >> /etc/supervisor/conf.d/app.conf && \
    echo 'autostart=true' >> /etc/supervisor/conf.d/app.conf && \
    echo 'autorestart=true' >> /etc/supervisor/conf.d/app.conf && \
    echo 'stderr_logfile=/var/log/supervisor/bot-err.log' >> /etc/supervisor/conf.d/app.conf && \
    echo 'stdout_logfile=/var/log/supervisor/bot-out.log' >> /etc/supervisor/conf.d/app.conf

# Expose the port for the Flask app
EXPOSE 8000

# Run both services using supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/app.conf"]
