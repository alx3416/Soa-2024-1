#!/usr/bin/env python
import sys
import time
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
count = 1
while True:
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message + str(count),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
        ))
    print(f" [x] Sent {message}" + str(count))
    count += 1
    time.sleep(1)
connection.close()
