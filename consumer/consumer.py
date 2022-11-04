from plyer import notification
import pika

server = '192.168.1.39'
currentPort = '5672'
#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('user','user')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=server, port=currentPort, credentials= credentials))
channel = connection.channel()
channel.exchange_declare('test', durable=True, exchange_type='topic')#defining callback functions responding to corresponding queue callbacks
def callbackFunctionForQueue(ch,method,properties,body):
 print('Message received from server: ', body)
channel.basic_consume(queue='comunicationQueue', on_message_callback=callbackFunctionForQueue, auto_ack=True)
#this will be command for starting the consumer session
channel.start_consuming()
notification.notify(
    title='Fin de simulación',
    message='La simulación ha finalizado')
