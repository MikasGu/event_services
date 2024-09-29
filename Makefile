.PHONY: install
install:
	poetry install

.PHONY: run-propagator
run-propagator:
	poetry run python cybercare_event_services/event_propagator/propagator.py --config cybercare_event_services/event_propagator/config.yaml

.PHONY: run-consumer
run-consumer:
	poetry run python cybercare_event_services/event_consumer/consumer.py --config cybercare_event_services/event_consumer/config.yaml
