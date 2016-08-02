import logging
import pika

logging.basicConfig()


class Consumer(object):
    """
    A RabbitMQ topic exchange consumer that will call the specified function
    when a message is received.
    """

    def __init__(self, host, exchange, callable):
        """
        Create a consumer instance and connection to RabbitMQ.
        """
        self.host = host
        self.exchange = exchange
        self.callable = callable
        #self.queue = ''
        self.queue = "dofinder"
        self.type = 'topic'
        self.channel = None
        self.consumer_tag = None

        self.parameters = pika.ConnectionParameters(host=self.host)
        self.connection = pika.SelectConnection(self.parameters,
                                                self.on_connected)

    def on_connected(self, connection):
        """
        Called by pika when a connection is established.
        """
        connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        """
        Called by pika when the channel is opened.
        """
        self.channel = channel
        self.channel.add_on_close_callback(self.on_channel_closed)
        self.channel.exchange_declare(self.on_exchange_declareok,
                                      exchange=self.exchange,
                                      type=self.type)

    def on_channel_closed(self, channel, reply_code, reply_text):
        """
        Called by pika when the channel is closed.
        """
        self.connection.close()

    def on_consumer_cancelled(self, frame):
        """
        Called by pika when the RabbitMQ connection is lost.
        """
        self.channel.close()

    def on_exchange_declareok(self, frame):
        """
        Called by pika when RabbitMQ has finished the Exchange.Declare
        command.
        """
        self.channel.queue_declare(self.on_queue_declareok, self.queue)

    def on_queue_declareok(self, frame):
        """
        Called by pika when RabbitMQ has finished the Queue.Declare
        command.
        """
        # Get the server assigned queue name
        #self.queue = frame.method.queue

        self.channel.queue_bind(self.on_bindok, queue=self.queue, exchange=self.exchange, routing_key="#")

    def on_bindok(self, frame):
        """
        Called by pika when RabbitMQ has finished the Queue.Bind command.
        Now it's safe to start consuming messages.
        """
        self.start_consuming()

    def start_consuming(self):
        """
        Start consuming messages.
        """
        self.channel.add_on_cancel_callback(self.on_consumer_cancelled)
        self.consumer_tag = self.channel.basic_consume(self.on_message,
                                                       self.queue)

    def stop_consuming(self):
        """
        Stop consuming messages.
        """
        self.channel.basic_cancel(self.on_cancelok, self.consumer_tag)

    def on_cancelok(self, frame):
        """
        Called by pika when RabbitMQ acknowledges the cancellation of a
        consumer.
        """
        self.connection.close()

    def on_message(self, channel, method, properties, body):
        """
        Called by pika when a message is delivered from RabbitMQ.  Call
        the specified function.
        """
        if self.callable:
            self.callable(body)

    def run(self):
        """
        Start the consumer event processing loop.
        """
        try:
            self.connection.ioloop.start()

        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        """
        Stop the event processing loop.
        """
        # Close the connection and restart the ioloop to allow the
        # process to terminate.
        self.stop_consuming()
        self.connection.ioloop.start()


def print_message(msg):
    """
    Print the message.
    """
    print(msg)

if __name__ == "__main__":
    c = Consumer('localhost', 'weather', print_message)
    c.run()