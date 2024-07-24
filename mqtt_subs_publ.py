import threading
import time
import paho.mqtt.client as mqtt
import random
import string
import signal

BROKER = 'localhost'
PORT = 1883
TOPIC = 'test/topic'
PAYLOAD_SIZE = 100  # tamanho do payload
PUBLISH_INTERVAL = 0.1  # intervalo de tempo entre publicações em segundos
RUN_TIME = 300  # tempo total de execução em segundos
INCREASE_INTERVAL = 1  # intervalo para aumentar threads em segundos

# Variável global para sinalizar quando parar
running = True

def generate_payload(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size))

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

def publisher(client_id, payload_size, interval):
    client = mqtt.Client(client_id)
    client.connect(BROKER, PORT, 60)
    while running:
        payload = generate_payload(payload_size)
        client.publish(TOPIC, payload)
        time.sleep(interval)
    client.disconnect()

def subscriber(client_id):
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    while running:
        client.loop()
    client.disconnect()

def stop_all(signum, frame):
    global running
    running = False
    print("Stopping all publishers and subscribers...")

if __name__ == "__main__":
    # Registrar o sinal de interrupção para parar o script
    signal.signal(signal.SIGINT, stop_all)

    threads = []
    publisher_count = 0
    subscriber_count = 0
    start_time = time.time()

    while running and (time.time() - start_time) < RUN_TIME:
        # Adicionar um novo publisher
        publisher_count += 1
        client_id_pub = f"publisher_{publisher_count}"
        t_pub = threading.Thread(target=publisher, args=(client_id_pub, PAYLOAD_SIZE, PUBLISH_INTERVAL))
        t_pub.start()
        threads.append(t_pub)
        print(f"Started publisher {publisher_count}")

        # Adicionar um novo subscriber
        subscriber_count += 1
        client_id_sub = f"subscriber_{subscriber_count}"
        t_sub = threading.Thread(target=subscriber, args=(client_id_sub,))
        t_sub.start()
        threads.append(t_sub)
        print(f"Started subscriber {subscriber_count}")

        # Espera pelo próximo aumento de threads
        time.sleep(INCREASE_INTERVAL)

    # Espera o tempo total de execução antes de parar todos os threads
    time.sleep(RUN_TIME - (time.time() - start_time))
    running = False
    print("Stopping all publishers and subscribers...")

    # Aguarda todos os threads terminarem
    for t in threads:
        t.join()

    print("All publishers and subscribers have stopped.")
