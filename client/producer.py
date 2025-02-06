import pika, json

params = pika.URLParameters('amqps://fsybomvm:gdfSDlLpMWJoDetGzdhlAM6frhXM1r-6@prawn.rmq.cloudamqp.com/fsybomvm')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)