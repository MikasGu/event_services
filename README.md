# Cybercare Event Services

This project implements a simple event-driven system with two services:

## Services Overview

- **Event Propagator:** Sends JSON events periodically.
- **Event Consumer:** Receives events and stores them (in a database or file).

## Installation

1. Clone the repository.
2. Install dependencies:
   poetry install

## Running the Services

- **Start the Propagator:**
   poetry run python cybercare_event_services/event_propagator/propagator.py --config cybercare_event_services/event_propagator/config.yaml

- **Start the Consumer:**
   poetry run python cybercare_event_services/event_consumer/consumer.py --config cybercare_event_services/event_consumer/config.yaml

## Configuration

Modify the `config.yaml` files for specific settings:

### Propagator Configuration

- `endpoint_url`
- `events_file`
- `interval_seconds`

### Consumer Configuration

- `storage_type`
- `file_path`
- `db_path`
- `endpoint_url`
- `port`

## Testing

1. Start the Consumer.
2. Start the Propagator.
3. Verify that events are stored in the database or file.
