import pika, json

connection_params = pika.URLParameters('amqps://fsybomvm:gdfSDlLpMWJoDetGzdhlAM6frhXM1r-6@prawn.rmq.cloudamqp.com/fsybomvm')

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

def publish(method, body):
    properties=pika.BasicProperties(method, delivery_mode=2)
    channel.basic_publish(
        exchange="",  
        routing_key="main",  
        body=json.dumps(body), 
        properties=properties
    )

    # channel.close()
    # connection.close()
