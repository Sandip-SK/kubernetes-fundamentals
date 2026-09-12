from flask import Flask, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import socket
import time

app = Flask(__name__)

# Total number of HTTP requests
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

# HTTP request latency
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


@app.before_request
def before_request():
    request.start_time = time.time()


@app.after_request
def after_request(response):
    duration = time.time() - request.start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.path,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.path
    ).observe(duration)

    return response


@app.route("/")
def home():
    return {
        "message": "Hello from Kubernetes! v2",
        "hostname": socket.gethostname()
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

@app.route("/error")
def error():
    return {"error": "Internal Server Error"}, 500

@app.route("/slow")
def slow():
    time.sleep(2)
    return {"message": "Slow response"}

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)