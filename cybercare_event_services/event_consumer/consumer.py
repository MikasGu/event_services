from flask import Flask, request, jsonify
import yaml
import argparse
import sqlite3
import os
import json
import logging


def load_config():
    parser = argparse.ArgumentParser(description="Event Consumer Service")
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    args = parser.parse_args()

    with open(args.config, 'r') as file:
        config = yaml.safe_load(file)

        config['storage_type'] = config.get('storage_type', 'sqlite')  # Default to sqlite

        if config['storage_type'] == 'sqlite':
            config['db_path'] = config.get('db_path', 'events.db')  # Default db path
        elif config['storage_type'] == 'file':
            config['file_path'] = config.get('file_path', 'events.log')  # Default file path
        else:
            raise ValueError(f"Invalid storage_type: {config['storage_type']}")

        return config


def init_db(config):
    if not os.path.exists(config['db_path']):
        try:
            conn = sqlite3.connect(config['db_path'])
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_payload TEXT NOT NULL
                )
            ''')
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
        finally:
            if conn:
                conn.close()


app = Flask(__name__)
config = load_config()
init_db(config)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/event', methods=['POST'])
def event_handler():
    event = request.get_json()
    logger.info(f"Received event: {event}")

    if isinstance(event, dict) and 'event_type' in event and 'event_payload' in event:
        logger.info(f"Valid event received: type: {event['event_type']}, payload: {event['event_payload']}")
        event_payload = event['event_payload']
        try:
            if config['storage_type'] == 'sqlite':
                conn = sqlite3.connect(config['db_path'])
                logger.info(f"Connected to database: {config['db_path']}")
                cursor = conn.cursor()

                event_payload_json = json.dumps(event_payload)
                logger.debug(f"Executing SQL: INSERT INTO events (event_type, event_payload) VALUES (?, ?), {(event['event_type'], event_payload_json)}")
                cursor.execute('INSERT INTO events (event_type, event_payload) VALUES (?, ?)',
                               (event['event_type'], event_payload_json))

                conn.commit()
                conn.close()
                logger.info(f"Event inserted successfully: {event}")
            elif config['storage_type'] == 'file':
                with open(config['file_path'], 'a') as f:
                    f.write(f"{json.dumps(event)}\n")
                logger.info(f"Event saved to file: {config['file_path']}")

            return jsonify({'status': 'success'}), 200
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            return jsonify({'error': 'Database error'}), 500
    else:
        logger.error(f"Invalid event format: {event}")
        return jsonify({'error': 'Invalid event format'}), 400


if __name__ == '__main__':
    app.run(port=config['port'])