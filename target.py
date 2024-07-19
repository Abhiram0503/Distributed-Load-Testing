# Import necessary libraries
from flask import Flask

app = Flask(__name__)

@app.route('/ping')
def ping():
    return "Pong"

@app.route('/metrics')
def metrics():
    # Implement logic to display metrics
    return "Metrics Endpoint"

if __name__ == '__main__':
    app.run(port=8000)
