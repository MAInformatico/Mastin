import pika
import os
import time
from checker import *

rabbitmq_user = os.environ.get('RABBITMQ_USER', 'guest')
rabbitmq_pass = os.environ.get('RABBITMQ_PASS', 'guest')
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 5672))
interval = int(os.environ.get('CHECK_INTERVAL', 300))  

def check_and_publish():
    reviewer = checker()
    hostList = reviewer.getHosts()
    if None in hostList:
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
        )
        channel = connection.channel()
        channel.exchange_declare(exchange='test', durable=True, exchange_type='topic')
        channel.queue_declare(queue='communicationQueue', durable=True)
        channel.queue_bind(exchange='test', queue='communicationQueue', routing_key='communicationQueue')

        message = 'One or more unknown devices have been discovered in our network!'
        channel.basic_publish(
            exchange='test',
            routing_key='communicationQueue',
            body=message
        )
        connection.close()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unknown device detected. Message published.")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] All devices known. Nothing to publish.")

if __name__ == '__main__':
    print(f"Producer started: {interval} seconds.")
    while True:
        check_and_publish()
        time.sleep(interval)