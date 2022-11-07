from plyer import notification
import pika

import os
import platform

server = 'IP server'
currentPort = 'your port'
#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials('user','userPass')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=server, port=currentPort, credentials= credentials))
channel = connection.channel()
channel.exchange_declare('test', durable=True, exchange_type='topic')#defining callback functions responding to corresponding queue callbacks

def callbackFunctionForQueue(ch,method,properties,body):
    lTitle = 'Warning'
    lMessage = body
    if platform.system() == 'Darwin':
        os.system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(lMessage, lTitle))
    else:
        notification.notify(
            title=lTitle,
            message = lMessage,
            app_icon='python.ico')
        

channel.basic_consume(queue='communicationQueue', on_message_callback=callbackFunctionForQueue, auto_ack=True)
#this will be command for starting the consumer session
channel.start_consuming()