# Mastin - Unknown Devices Detector

**Mastin** is a lightweight network monitoring tool that detects unknown devices on a local network in real time.

## Problem

In small networks, new or unauthorized devices can connect without notice. Traditional monitoring tools are often heavy, complex, or require external services.

## Solution

Mastin uses a pub/sub architecture with RabbitMQ to process network events and alert when an unknown device is detected.

## Architecture

Device scan → event published to RabbitMQ → consumer processes event → alert if unknown device.

## Technologies

- Python
- RabbitMQ (pub/sub pattern)
- Sockets
- Docker

## How to run it
```bash
docker-compose up
```
## What I learned
- Designing an event-driven system with pub/sub.
- Using sockets for network discovery in Python.
- Containerizing services with Docker for easy deployment.

## Future work
- Add a web dashboard for real-time visualization.
- Add support for multiple network ranges.
- Add persistent storage of detected devices.