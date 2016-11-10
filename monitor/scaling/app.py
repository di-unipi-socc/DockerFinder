from flask import Flask, Response
import pika
import os
import socket
import time

app = Flask(__name__)

# Enable debugging if the DEBUG environment variable is set and starts with Y
# app.debug = os.environ.get("DEBUG", "").lower().startswith('y')
#
hostname = socket.gethostname()
#
# urandom = os.open("/dev/urandom", os.O_RDONLY)


@app.route("/")
def index():
    c = count_queue_msg()

    return "number of queues " +str(c)
    #return "RNG running on {}\n".format(hostname)


@app.route("/<int:how_many_bytes>")
def rng(how_many_bytes):
    # Simulate a little bit of delay
    time.sleep(0.1)
    return Response(
        os.read(urandom, how_many_bytes),
        content_type="application/octet-stream")

def count_queue_msg():
    #docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dockerfinder_rabbitmq_1
    # rabbit_container_name = 'dockerfinder_rabbitmq_1'
    # nmap_out = subprocess.run(['docker inspect --format "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" '+ rabbit_container_name],
    # #"docker", "inspect", "--format", '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"', "dockerfinder_rabbitmq_1"],
    #                 shell=True,
    #                 stdout=subprocess.PIPE,
    #                 stderr=subprocess.PIPE)
    # ip_rabbit  = nmap_out.stdout.decode("utf-8").rstrip()
    #
    # #print("ip rabbit "+str(ip_rabbit)
    # url = "amqp://guest:guest@"+ip_rabbit+":5672"
    url = "amqp://guest:guest@rabbitmq:5672"
    queue= "images"
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

    c = queue.method.message_count
    return c

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
