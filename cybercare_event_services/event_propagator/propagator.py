import requests
import os
import random
import time
import yaml
import json
import argparse


def load_config():
    parser = argparse.ArgumentParser(description="Event Propagator Service")
    parser.add_argument('--config', default='config.yaml')
    args = parser.parse_args()

    try:
        with open(args.config, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError as e:
        print(f"Error: Configuration file not found - {args.config}")
        raise e  # Re-raise the exception to halt execution



def send_event(events, config):
    event = random.choice(events)
    try:
        response = requests.post(config['endpoint_url'], json=event)
        response.raise_for_status()
        print(f"Sent event: {event} | Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send event: {e}")


def main():
    config = load_config()

    config['events_file'] = os.path.join(os.path.dirname(__file__), 'events.json')

    with open(config['events_file'], 'r') as file:
        events = json.load(file)

    while True:
        send_event(events, config)
        time.sleep(config['interval_seconds'])


if __name__ == "__main__":
    main()
