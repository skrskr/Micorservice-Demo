import pika, json

# params = pika.URLParameters("amqp://myuser:mypassword@rabbitmq:5672/")
params = pika.URLParameters("amqp://myuser:mypassword@192.168.0.107:5672/")


connection = pika.BlockingConnection(params)


channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)


