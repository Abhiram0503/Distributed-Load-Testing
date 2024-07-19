# app.py
from flask import Flask, render_template
from flask_socketio import SocketIO
from kafka import KafkaConsumer

app = Flask(__name__)
socketio = SocketIO(app)

# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic = 'metrics_final'

consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers, group_id='metrics_group')

@app.route('/')
def index():
    return render_template('index.html')

def listen_to_kafka():
    for message in consumer:
        socketio.emit('new_message', {'message': message.value.decode('utf-8')})

if __name__ == '__main__':
    socketio.start_background_task(target=listen_to_kafka)
    socketio.run(app)
