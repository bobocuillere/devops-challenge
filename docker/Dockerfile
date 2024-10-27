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

# Build the .deb package
CMD dpkg-deb --build /build prometheus-postgres-exporter.deb
