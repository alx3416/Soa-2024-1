import pika
import time
import proto.mi_mensaje_pb2 as mi_mensaje_pb2

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel2 = connection.channel()

channel.queue_declare(queue='hello')
channel2.queue_declare(queue='hello again')
counter = 1
protobuf_message = mi_mensaje_pb2.HelloWorld()
channel.exchange_declare(exchange='direct_logs',
                         exchange_type='direct')
channel2.exchange_declare(exchange='direct_logs2',
                         exchange_type='direct')
severity = "warning"
while True:
    protobuf_message.name = "fulano menganillo"
    protobuf_message.id = counter
    protobuf_message.msg = -123.456
    protobuf_message.state = True
    rabbit_message = protobuf_message.SerializeToString()

    print(" [x] Sent proto message: " + str(counter) + " severity: " + severity)
    time.sleep(3)
    counter = counter + 1
    if severity == "warning":
        channel.basic_publish(exchange='direct_logs',
                              routing_key=severity, body=rabbit_message)
        severity = "pass"
    else:
        channel2.basic_publish(exchange='direct_logs2',
                              routing_key=severity, body=rabbit_message)
        severity = "warning"

connection.close()
