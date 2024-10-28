# File: docker/Dockerfile

ARG DEBIAN_VERSION
FROM debian:${DEBIAN_VERSION}

# Install dependencies needed to build .deb packages
RUN apt-get update && \
    apt-get install -y dpkg-dev build-essential wget

# Set work directory
WORKDIR /build

# Define the version and architecture
ARG EXPORTER_VERSION=0.15.0
ARG ARCHITECTURE=linux-amd64

# Download prometheus-postgres-exporter for a specific version and architecture
RUN wget https://github.com/prometheus-community/postgres_exporter/releases/download/v${EXPORTER_VERSION}/postgres_exporter-${EXPORTER_VERSION}.${ARCHITECTURE}.tar.gz && \
    tar -xzvf postgres_exporter-${EXPORTER_VERSION}.${ARCHITECTURE}.tar.gz && \
    mv postgres_exporter-${EXPORTER_VERSION}.${ARCHITECTURE}/postgres_exporter /usr/local/bin/

# Create the DEBIAN directory and add the control file
RUN mkdir -p /build/DEBIAN && \
    echo "Package: prometheus-postgres-exporter" > /build/DEBIAN/control && \
    echo "Version: ${EXPORTER_VERSION}" >> /build/DEBIAN/control && \
    echo "Architecture: amd64" >> /build/DEBIAN/control && \
    echo "Maintainer: Sophnel <sophnel.merzier@sinch.com>" >> /build/DEBIAN/control && \
    echo "Description: Prometheus exporter for PostgreSQL metrics" >> /build/DEBIAN/control

# Build the .deb package and place it in a known location
RUN mkdir -p /workspace/deb_build && \
    dpkg-deb --build /build /workspace/deb_build/prometheus-postgres-exporter.deb
