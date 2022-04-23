import pdfkit
import pika
import os

def get_pdf_stats(id: int):
    os.system(f"rm -rf /user/src/worker/pdfs/{id}-stats.pdf")
    pdfkit.from_url(f'http://app.rest.com:5000/users/{id}', f'/user/src/worker/pdfs/{id}-stats.pdf')


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', heartbeat=0))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    get_pdf_stats(int(body.decode()))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()