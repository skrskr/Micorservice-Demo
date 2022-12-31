import pika, json, django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from products.models import Product

params = pika.URLParameters("amqp://myuser:mypassword@192.168.0.107:5672/")


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("recieved in admin")
    content_type = properties.content_type
    if content_type == 'product_liked':
        product_id = json.loads(body)
        product = Product.objects.get(id=product_id)
        product.likes = product.likes + 1
        product.save()
        print("product liked success")
        


channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print("start consumeing")
channel.start_consuming()

channel.close()