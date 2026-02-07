from flask import Flask, jsonify
import redis
import time
import socket
import os
import logging
import threading

# ---------- LOGGING SETUP ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)
# ----------------------------------

app = Flask(__name__)
hostname = socket.gethostname()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MESSAGE = os.getenv("MESSAGE", "HELLO Martian from Redis + Flask!!!")

# ✅ Create Redis client ONCE, with timeouts
r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
    retry_on_timeout=False
)

# ---------- SAFE REDIS HELPERS ----------
def safe_redis_get(key):
    try:
        return r.get(key)
    except Exception as e:
        logger.error(f"Redis GET failed: {e}")
        return None

def safe_redis_set(key, value):
    try:
        r.set(key, value)
        return True
    except Exception as e:
        logger.warning(f"Redis SET failed: {e}")
        return False
# --------------------------------------

@app.route("/message", methods=["GET"])
def get_message():
    value = safe_redis_get("message")

    if value is None:
        return jsonify({
            "error": "Service temporarily unavailable",
            "served_by": hostname
        }), 503

    logger.info(f"/message served by {hostname}")
    return jsonify({
        "message": value,
        "served_by": hostname
    })

def update_redis():
    while True:
        safe_redis_set(
            "message",
            f"{MESSAGE} ({int(time.time())})"
        )
        time.sleep(10)

if __name__ == "__main__":
    t = threading.Thread(target=update_redis, daemon=True)
    t.start()

    logger.info("Flask app starting on port 5000")
    app.run(host="0.0.0.0", port=5000)
