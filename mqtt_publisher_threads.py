import paho.mqtt.client as mqtt
import time
import argparse
import threading
import psutil

# Global variable to count the number of messages published
message_count = 0
message_count_lock = threading.Lock()

def publish_messages(broker, topic, frequency, message, client_id):
    client = mqtt.Client(client_id=client_id)
    client.connect(broker)

    interval = 1.0 / frequency  # Calculate interval in seconds

    try:
        while True:
            client.publish(topic, message)
            with message_count_lock:
                global message_count
                message_count += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"Stopping publisher {client_id}")
    finally:
        client.disconnect()

def start_publisher_thread(broker, topic, frequency, message, client_id_prefix, thread_num):
    client_id = f"{client_id_prefix}_{thread_num}"
    thread = threading.Thread(target=publish_messages, args=(broker, topic, frequency, message, client_id))
    thread.daemon = True
    thread.start()
    return thread

def monitor_system_resources(interval=1):
    cpu_usage = psutil.cpu_percent(interval=interval)
    memory_info = psutil.virtual_memory()
    return cpu_usage, memory_info.percent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Publisher with Threads")
    parser.add_argument("--broker", type=str, required=True, help="MQTT broker address")
    parser.add_argument("--topic", type=str, required=True, help="MQTT topic")
    parser.add_argument("--frequency", type=float, required=True, help="Publishing frequency per thread (messages per second)")
    parser.add_argument("--message", type=str, default="Test message", help="Message to publish")
    parser.add_argument("--client-id-prefix", type=str, default="mqtt_publisher", help="Client ID prefix for MQTT")
    parser.add_argument("--start-threads", dest="start_threads", type=int, default=1, help="Starting number of publisher threads")
    parser.add_argument("--max-threads", dest="max_threads", type=int, required=True, help="Maximum number of publisher threads")
    parser.add_argument("--duration", type=int, default=60, help="Duration to run each test step in seconds")

    args = parser.parse_args()

    current_threads = args.start_threads

    while current_threads <= args.max_threads:
        print(f"Starting test with {current_threads} threads")
        threads = []
        for i in range(current_threads):
            thread = start_publisher_thread(args.broker, args.topic, args.frequency, args.message, args.client_id_prefix, i)
            threads.append(thread)

        # Let the threads run for a while to stabilize and measure resource usage
        start_time = time.time()
        message_count = 0

        while time.time() - start_time < args.duration:
            cpu_usage, memory_usage = monitor_system_resources(interval=1)
            with message_count_lock:
                current_message_count = message_count

            print(f"Threads: {current_threads} | CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | Messages Published: {current_message_count}")

        # Increment the number of threads for the next iteration
        current_threads += 1

        # Wait before starting the next increment to avoid overloading the system too quickly
        time.sleep(5)

    print("Test completed")
