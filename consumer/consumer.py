import pika
import os
import platform
from plyer import notification


rabbitmq_user = os.environ.get('RABBITMQ_USER', 'guest')
rabbitmq_pass = os.environ.get('RABBITMQ_PASS', 'guest')
rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_port = int(os.environ.get('RABBITMQ_PORT', 5672))

# RabbitMQ connection setup
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=rabbitmq_host, port=rabbitmq_port, credentials=credentials)
)
channel = connection.channel()
channel.exchange_declare('test', durable=True, exchange_type='topic')

def callbackFunctionForQueue(ch, method, properties, body):
    lTitle = 'Warning'
    lMessage = body.decode()  
    if platform.system() == 'Darwin':
        os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(lMessage, lTitle))
    else:
        notification.notify(
            title=lTitle,
            message=lMessage,
            app_icon='python.ico'
        )

channel.queue_declare(queue='communicationQueue', durable=True)
channel.queue_bind(exchange='test', queue='communicationQueue', routing_key='communicationQueue')
channel.basic_consume(queue='communicationQueue', on_message_callback=callbackFunctionForQueue, auto_ack=True)
channel.start_consuming()