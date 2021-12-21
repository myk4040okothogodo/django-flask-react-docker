import pika
import io
import json
from main import Product, db

params = pika.URLParameters('amqps://jhczkzcj:xpCcgMGYCBgS-7_dVM1XS2m9sUdyMdmM@snake.rmq2.cloudamqp.com/jhczkzcj')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    print(body)
    data = json.loads(body)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title= data['title'], image= data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = date['image']
        db.session.commit()
        print('Product updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product deleted')


channel.basic_consume(queue='main',on_message_callback=callback)

print("started Consuming")

channel.start_consuming()
channel.close()
