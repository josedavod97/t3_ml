import json
import os
from pathlib import Path

from flask import Flask, Response, send_from_directory


FRONTEND_DIR = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=None)


@app.get("/")
@app.get("/app")
def read_app() -> Response:
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/config.js")
def read_config() -> Response:
    backend_url = os.getenv("BACKEND_URL")
    if not backend_url:
        return Response("BACKEND_URL is not configured", status=503, mimetype="text/plain")

    config = f"window.CASAVALOR_API_URL = {json.dumps(backend_url.rstrip('/'))};"
    return Response(
        config,
        mimetype="application/javascript",
        headers={"Cache-Control": "no-store"},
    )


@app.get("/static/<path:filename>")
def read_static_file(filename: str) -> Response:
    return send_from_directory(FRONTEND_DIR, filename)
