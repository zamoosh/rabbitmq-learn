import time, pika, threading


def producer_1():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='q1')

    c = 0
    while True:
        s = f'Hello World!'
        channel.basic_publish(exchange='', routing_key='q1', body=s.encode('ascii'))

        time.sleep(1)
        print(f'producer_1: {c}')
        c += 1

    connection.close()


def producer_2():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='q2')

    c = 0
    while True:
        s = f'Good Bye World!'
        channel.basic_publish(exchange='', routing_key='q2', body=s.encode('ascii'))

        time.sleep(1)
        print(f'producer_2: {c}')
        c += 1

    connection.close()


if __name__ == '__main__':
    p1 = threading.Thread(target=producer_1, daemon=True)
    p1.start()

    p2 = threading.Thread(target=producer_2, daemon=True)
    p2.start()

    p1.join()
    p2.join()

    # connection.close()
