import pika, json, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trabalho_2.settings')  

django.setup()

from products.models import Product

params = pika.URLParameters('amqps://fsybomvm:gdfSDlLpMWJoDetGzdhlAM6frhXM1r-6@prawn.rmq.cloudamqp.com/fsybomvm')

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        if properties.content_type == 'product_rated':
            id = data.get('id')
            product = Product.objects.get(id=id)
            rating = data.get('rating') 

            product.total_ratings += rating
            product.ratings_count += 1
            product.save()

            print(f'Product {id} received a new rating of {rating}')
        elif properties.content_type == 'product_liked':
            product = Product.objects.get(id=data)
            product.likes = product.likes + 1
            product.save()

            print(f'Product {data} likes +1')
        else:
            print(f"Unknown message type: {properties.content_type}")

    except Product.DoesNotExist:
        print(f"Product with id {data} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

