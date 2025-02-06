import pika, json
from main import Product, db

params = pika.URLParameters('amqps://fsybomvm:gdfSDlLpMWJoDetGzdhlAM6frhXM1r-6@prawn.rmq.cloudamqp.com/fsybomvm')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print(f" [x] Received {body} in main")
    body = int(body) if isinstance(body, str) else body
    d = json.loads(body)

    if properties.content_type == 'product_created':
        product = Product(id=d['id'], title=d['title'], image=d['image'])
        db.session.add(product)
        db.session.commit()
        print(f" [x] Product {product.title} id:{product.id} created")

    elif properties.content_type == 'product_updated':
        product = db.session.get(Product, d['id'])
        if product:
            product.title = d['title']
            product.image = d['image']
            product.likes = d['likes']
            db.session.commit()
            print(f" [x] Product {product.title} id:{product.id} updated")
        else:
            print(f" [x] Product {d['id']} not found, unable to update")

    elif properties.content_type == 'product_deleted':
        # product = db.session.get(Product, body)
        product = Product.query.get(d)
        if product:
            db.session.delete(product)
            db.session.commit()
            print(f" [x] Product {product.title} id:{product.id} deleted")
        else:
            print(f" [x] Product {d['id']} not found, nothing to delete")

channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')
channel.start_consuming()

# channel.close()
