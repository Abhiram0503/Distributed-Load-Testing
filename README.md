# Distributed Testing and Monitoring System

This repository contains Python scripts (`orc.py`, `driver.py`, `server.py`, and `target.py`) that simulate a distributed testing and monitoring system utilizing Kafka and Flask for message passing and communication. The system orchestrates the registration and management of drivers, conducts tests, triggers tests based on configurations, and receives metrics from the drivers.

## Project Overview

### `orc.py` (Orchestrator)

- **Description**: The orchestrator script coordinates driver registration, test configuration, and triggering tests based on provided configurations.
- **Functions**:
    - `register()`: Processes driver registrations from the Kafka `register` topic and starts test configuration once all drivers are registered.
    - `test_config()`: Sends test configuration to the Kafka `test_config` topic.
    - `trigger()`: Sends trigger messages to the Kafka `trigger` topic to start tests for drivers.
    - `metrics()`: Listens to the Kafka `metrics` topic for metrics data and prints them.
    - `HeartbeatReceiver` class: Monitors the Kafka `heartbeat` topic for driver heartbeats and restarts registration if a driver stops sending heartbeats.
- **Usage**: Run the script with arguments: number of drivers, test type, test message delay, and message count per delay.

### `driver.py` (Driver)

- **Description**: The driver script simulates driver nodes that receive configurations and triggers from the orchestrator and send metrics data back to the orchestrator.
- **Functions**:
    - `register()`: Registers the driver with the orchestrator by sending a message to the Kafka `register` topic.
    - `test_config()`: Listens to the Kafka `test_config` topic for test configurations and updates the driver's configurations.
    - `trigger()`: Listens to the Kafka `trigger` topic for trigger messages and starts the avalanche testing process.
    - `avalanche()`: Conducts the avalanche testing process and sends metrics data to the Kafka `metrics` topic.
- **Usage**: Run the script to start the driver node. It will automatically handle registration, receiving configurations, and triggers.

### `server.py` (Flask Server for Metrics)

- **Description**: This script provides a web server using Flask and listens to Kafka metrics messages to display them on a web interface.
- **Functions**:
    - `index()`: Serves the main HTML page (`index.html`) for displaying metrics.
    - `listen_to_kafka()`: Listens to the Kafka `metrics_final` topic and emits new messages through WebSockets.
- **Usage**: Run the script to start the server and listen for metrics data from Kafka. It automatically updates the web interface with new messages.

### `target.py` (Target Server for Requests)

- **Description**: This script provides a simple web server using Flask to handle ping and metrics requests.
- **Functions**:
    - `ping()`: Returns a "Pong" response to ping requests.
    - `metrics()`: Placeholder endpoint for displaying metrics.
- **Usage**: Run the script to start the server and listen for incoming requests.

## Requirements

- Python 3.x
- Kafka and related libraries (`kafka-python`)
- `requests` library for HTTP requests
- Flask for web server functionality
- Flask-SocketIO for real-time communication in `server.py`

## Setup and Execution

1. Start Kafka and ensure it is running on the default port (`localhost:9092`).
2. Run the orchestrator script (`orc.py`) with the required arguments: number of drivers, test type, test message delay, and message count per delay.
    ```shell
    python orc.py <num_of_drivers> <test_ty> <test_msg_delay> <msg_count_per_delay>
    ```
3. Run the driver script (`driver.py`) to simulate the driver nodes.
    ```shell
    python driver.py
    ```
4. Run the Flask server (`server.py`) to display the metrics data.
    ```shell
    python server.py
    ```
5. Run the target server (`target.py`) to handle ping and metrics requests.
    ```shell
    python target.py
    ```

## Notes

- The orchestrator, driver, server, and target scripts should be run concurrently.
- Ensure that Kafka and Flask are set up and running before executing the scripts.
- The Flask server serves the main web page (`index.html`) to display metrics data in real-time using WebSockets.
