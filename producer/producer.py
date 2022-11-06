import pika
from checker import *

reviewer = checker()

hostList = reviewer.getHosts()
if None in hostList:
    credentials = pika.PlainCredentials('user','userPass')
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))
    channel= connection.channel()
    channel.exchange_declare('communicationQueue', durable=True, exchange_type='topic')
    channel.queue_declare(queue= 'communicationQueue')
    channel.queue_bind(exchange='communicationQueue', queue='communicationQueue', routing_key='communicationQueue')
    message = 'One or more unknown devices have been discovered in our network!'
    channel.basic_publish(exchange='communicationQueue', routing_key='communicationQueue', body= message)
    channel.close()
else:
    pass
