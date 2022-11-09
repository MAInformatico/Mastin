from plyer import notification
import pika

import os
import platform

def readFile(thefile):
    with open(str(thefile),'r') as f:
        info = []        
        for line in f:            
            info.append(line.rstrip())
    return info

connectionData = readFile('connectionData.txt')

#declaring the credentials needed for connection like host, port, username, password, exchange etc
credentials = pika.PlainCredentials(connectionData[0],connectionData[1])
connection = pika.BlockingConnection(pika.ConnectionParameters(host=connectionData[2], port=connectionData[3], credentials= credentials))
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