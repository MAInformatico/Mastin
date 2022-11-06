import pika
from checker import *

reviewer = checker()

hostList = reviewer.getHosts()
print (hostList)
if None in hostList:
    credentials = pika.PlainCredentials('user','userPass')
    connection= pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials= credentials))
    channel= connection.channel()
    channel.exchange_declare('comunicationQueue', durable=True, exchange_type='topic')
    channel.queue_declare(queue= 'comunicationQueue')
    channel.queue_bind(exchange='comunicationQueue', queue='comunicationQueue', routing_key='comunicationQueue')
    message = 'One or more unknown devices have been discovered in our network!'
    channel.basic_publish(exchange='comunicationQueue', routing_key='comunicationQueue', body= message)
    channel.close()
else:
    pass
