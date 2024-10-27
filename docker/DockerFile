# File: Dockerfile
FROM debian:${DEBIAN_VERSION} 

# Install dependencies needed to build .deb packages
RUN apt-get update && \
    apt-get install -y dpkg-dev build-essential wget

# Set work directory
WORKDIR /build

# Download prometheus-postgres-exporter
RUN wget https://github.com/prometheus-community/postgres_exporter/releases/latest/download/postgres_exporter

# Build the .deb package
CMD dpkg-deb --build /build prometheus-postgres-exporter.deb
