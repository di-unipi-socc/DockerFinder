from flask import Flask, Response,request, jsonify, url_for
import pika
import sys
import os
import socket

app = Flask(__name__)

# Enable debugging if the DEBUG environment variable is set and starts with Y
# app.debug = os.environ.get("DEBUG", "").lower().startswith('y')
#
hostname = socket.gethostname()

# urandom = os.open("/dev/urandom", os.O_RDONLY)

@app.route('/')
def index():
    url = ""
    with app.test_request_context():
        url = url_for('service', servicename="rabbitmq", queuename="images")
    return url


@app.route('/service/<servicename>/queue/<queuename>')
def service(servicename, queuename):
    try:
        msg_count = count_queue_msg(servicename,queuename)
        return jsonify(
                err=False,
                service=servicename,
                load=msg_count,
                queue=queuename
                )
    except :
        return jsonify(
                err=True,
                msg="Error in connecting"+servicename
                )




def count_queue_msg(service, queue):

    url = "amqp://guest:guest@"+service+":5672"
    print("connecting to : " +url)
    connection = pika.BlockingConnection(pika.URLParameters(url))
    # Open the channel
    channel = connection.channel()
    # Declare the queue
    queue =  channel.queue_declare(queue=queue,
                    passive=True,
                    durable=True,
                    exclusive=False,
                    auto_delete=False
                    )

    connection.close()
    c = queue.method.message_count
    return c

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3002)
