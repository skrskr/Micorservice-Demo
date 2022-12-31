import pika, json

from main import Product, db
params = pika.URLParameters("amqp://myuser:mypassword@192.168.0.107:5672/")


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print("recieive in main")
    data = json.loads(body)
    print(data)
    content_type = properties.content_type
    print(content_type)
    
    if content_type == 'product_created':
        print("created")
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        
    elif content_type == 'product_updated':
            print("updated")
            product =Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
            
    elif content_type == 'product_deleted':
        print("deleted")
        product =Product.query.get(data)
        db.session.delete(product)
        db.session.commit()


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print("start consumeing")
channel.start_consuming()

channel.close()