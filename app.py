from flask import Flask, jsonify
import redis
import time
import socket
import os
import logging
import threading

# ---------- LOGGING SETUP (MUST BE FIRST) ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)
# --------------------------------------------------

app = Flask(__name__)

hostname = socket.gethostname()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MESSAGE = os.getenv("MESSAGE", "HELLO Martian from Redis + Flask!!!")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

r.set("message", MESSAGE)

@app.route("/message", methods=["GET"])
def get_message():
    value = r.get("message")

    logger.info(f"/message served by {hostname}")

    return jsonify({
        "message": value,
        "served_by": hostname
    })

def update_redis():
    while True:
        r.set("message", f"{MESSAGE} ({int(time.time())})")
        logger.info("Redis message updated")
        time.sleep(10)

if __name__ == "__main__":
    t = threading.Thread(target=update_redis, daemon=True)
    t.start()

    logger.info("Flask app starting on port 5000")
    app.run(host="0.0.0.0", port=5000)
