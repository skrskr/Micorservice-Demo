import pika

params = pika.URLParameters("amqp://myuser:mypassword@192.168.0.107:5672/")


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("recieive in admin")
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("start consumeing")
channel.start_consuming()

channel.close()