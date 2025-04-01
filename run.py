import os
import subprocess
import sys
import logging
import time
import signal
import threading

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Store the processes
processes = []

def signal_handler(sig, frame):
    logger.info("Shutdown signal received, stopping all processes...")
    for process in processes:
        if process.poll() is None:  # If process is still running
            process.terminate()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_flask():
    try:
        logger.info("Starting Flask app...")
        flask_process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        processes.append(flask_process)
        return flask_process
    except Exception as e:
        logger.error(f"Failed to start Flask app: {str(e)}")
        return None

def start_bot():
    try:
        logger.info("Starting Telegram bot...")
        bot_process = subprocess.Popen(
            [sys.executable, "-m", "Restriction"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        processes.append(bot_process)
        return bot_process
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {str(e)}")
        return None

def log_stream(stream, prefix):
    for line in stream:
        if line:
            logger.info(f"[{prefix}] {line.strip()}")

def monitor_process(process, name):
    # Create threads to log stdout and stderr
    stdout_thread = threading.Thread(
        target=log_stream, 
        args=(process.stdout, f"{name} OUT")
    )
    stderr_thread = threading.Thread(
        target=log_stream, 
        args=(process.stderr, f"{name} ERR")
    )
    
    stdout_thread.daemon = True
    stderr_thread.daemon = True
    
    stdout_thread.start()
    stderr_thread.start()
    
    return_code = process.wait()
    
    # Wait for logging threads to finish
    stdout_thread.join()
    stderr_thread.join()
    
    if return_code != 0:
        logger.error(f"{name} process exited with code {return_code}")
        return False
    return True

if __name__ == "__main__":
    try:
        flask_process = start_flask()
        # Give Flask a moment to start up
        time.sleep(2)
        
        bot_process = start_bot()
        
        if flask_process and bot_process:
            logger.info("All services started successfully!")
            
            # Start monitoring threads
            flask_thread = threading.Thread(
                target=monitor_process, 
                args=(flask_process, "FLASK")
            )
            bot_thread = threading.Thread(
                target=monitor_process, 
                args=(bot_process, "BOT")
            )
            
            flask_thread.daemon = True
            bot_thread.daemon = True
            
            flask_thread.start()
            bot_thread.start()
            
            # Monitor processes
            while True:
                if flask_process.poll() is not None:
                    logger.error("Flask process has terminated unexpectedly")
                    # Capture any remaining stderr
                    errors = flask_process.stderr.read()
                    if errors:
                        logger.error(f"Flask error output: {errors}")
                    signal_handler(None, None)
                    break
                
                if bot_process.poll() is not None:
                    logger.error("Bot process has terminated unexpectedly")
                    # Capture any remaining stderr
                    errors = bot_process.stderr.read()
                    if errors:
                        logger.error(f"Bot error output: {errors}")
                    signal_handler(None, None)
                    break
                
                time.sleep(1)
        else:
            logger.error("Failed to start one or more services")
            signal_handler(None, None)
    
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
        signal_handler(None, None)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        signal_handler(None, None) 