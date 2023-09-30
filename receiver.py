import time

import pika
import threading


def recv_1():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [X][q1] Received {body.decode('ascii')}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.queue_declare(queue='q1')
    channel.basic_consume(queue='q1', on_message_callback=callback)
    channel.start_consuming()


def recv_2():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        print(f" [Y][q2] Received {body.decode('ascii')}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    # channel.queue_declare(queue='q2')
    channel.basic_consume(queue='q2', on_message_callback=callback)
    channel.start_consuming()


def counting():
    c = 0
    while c < 50:
        print(f'c in counter: {c}')
        time.sleep(1)
        c += 1


if __name__ == '__main__':
    # t = threading.Thread(target=counting, daemon=True)
    # t.start()

    rec_1 = threading.Thread(target=recv_1, daemon=True)
    rec_1.start()

    rec_2 = threading.Thread(target=recv_2, daemon=True)
    rec_2.start()

    rec_1.join()
    rec_2.join()
