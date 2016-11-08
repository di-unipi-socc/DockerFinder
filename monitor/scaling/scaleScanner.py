import pika


class ScaleScanner:

    def __init__(self, amqp_url, queue):
        self._url= amqp_url
        self._queue=queue

    def count_queue_msg(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(self._url))
        # Open the channel
        channel = self.connection.channel()
        # Declare the queue
        queue =  channel.queue_declare(queue=self._queue,
                        passive=True,
                        durable=True,
                        exclusive=False,
                        auto_delete=False
                        )

        c = queue.method.message_count
        return c

if __name__ == '__main__':
    scaling = ScaleScanner('amqp://guest:guest@rabbitmq:5672','images')

    for i in range(10):
        ci = scaling.count_queue_msg()
        print(str(ci)+ " :images in the queue")
