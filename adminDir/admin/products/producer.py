import pika
import json

params = pika.URLParameters('amqps://jhczkzcj:xpCcgMGYCBgS-7_dVM1XS2m9sUdyMdmM@snake.rmq2.cloudamqp.com/jhczkzcj')
connection= pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body = json.dumps(body), properties=properties)
