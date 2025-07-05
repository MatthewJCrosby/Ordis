#!/bin/bash

set -e  # exit on any error

echo "🔧 Checking for Docker..."

if ! command -v docker &> /dev/null; then
    echo "📦 Docker not found. Installing Docker..."
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl enable --now docker
    echo "✅ Docker installed."
else
    echo "✅ Docker already installed."
fi

echo "🔧 Checking for Docker Compose plugin..."

if ! docker compose version &> /dev/null; then
    echo "📦 Docker Compose plugin not found. Installing..."
    sudo apt install -y docker-compose-plugin
    echo "✅ Docker Compose plugin installed."
else
    echo "✅ Docker Compose plugin already installed."
fi

echo "📄 Setting up environment..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created from template."
else
    echo "✅ .env already exists."
fi

echo "🐳 Starting Docker containers..."

docker compose up --build
