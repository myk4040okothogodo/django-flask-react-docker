import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_settings")
django.setup()

from products.models import Product



params = pika.URLParameters('amqps://jhczkzcj:xpCcgMGYCBgS-7_dVM1XS2m9sUdyMdmM@snake.rmq2.cloudamqp.com/jhczkzcj')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    uid = json.loads(body)
    print(id)

    product = Product.objects.get(id=uid['id'])
    product.likes +=  1
    product.save()
    print("Product likes increased.")


channel.basic_consume(queue='admin',on_message_callback=callback)

print("started Consuming")

channel.start_consuming()
channel.close()


#start with rebuilding containers tommorow
