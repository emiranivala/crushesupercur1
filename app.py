import os
import logging
from flask import Flask, jsonify

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    logger.info("Health check request received")
    return "crushe Bot is Running!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
