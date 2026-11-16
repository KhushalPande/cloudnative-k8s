import os
import socket
import platform
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

APP_NAME = "CloudNative Notes"
VERSION = os.getenv("APP_VERSION", "1.0")
ENVIRONMENT = os.getenv("APP_ENV", "development")
MESSAGE = os.getenv("APP_MESSAGE", "Hello from a container!")
STARTED = datetime.now(timezone.utc)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ app_name }}</title>
  <style>
    body { font-family: Arial, sans-serif; background:#0f172a; color:#e2e8f0; margin:0; }
    .wrap { max-width: 720px; margin: 60px auto; padding: 0 20px; text-align:center; }
    h1 { color:#38bdf8; margin-bottom: 4px; }
    .card { background:#1e293b; border-radius:10px; padding:20px; margin:18px 0; }
    .pod { font-size:1.5em; color:#4ade80; font-family: monospace; word-break: break-all; }
    table { width:100%; border-collapse:collapse; margin-top:10px; }
    td { padding:6px 10px; border-bottom:1px solid #334155; text-align:left; }
    td:first-child { color:#94a3b8; width:40%; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>{{ app_name }}</h1>
    <p>{{ message }}</p>
    <div class="card">
      <div>Served by container / pod</div>
      <div class="pod">{{ hostname }}</div>
      <small>Refresh the page - with several replicas this name changes (load balancing).</small>
    </div>
    <div class="card">
      <table>
        <tr><td>Version</td><td>{{ version }}</td></tr>
        <tr><td>Environment</td><td>{{ environment }}</td></tr>
        <tr><td>Python</td><td>{{ python }}</td></tr>
        <tr><td>Started (UTC)</td><td>{{ started }}</td></tr>
      </table>
    </div>
  </div>
</body>
</html>"""


@app.route("/")
def home():
    return render_template_string(
        PAGE,
        app_name=APP_NAME,
        message=MESSAGE,
        hostname=socket.gethostname(),
        version=VERSION,
        environment=ENVIRONMENT,
        python=platform.python_version(),
        started=STARTED.strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/api/info")
def info():
    return jsonify(
        app=APP_NAME,
        version=VERSION,
        environment=ENVIRONMENT,
        pod=socket.gethostname(),
        started=STARTED.isoformat(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
