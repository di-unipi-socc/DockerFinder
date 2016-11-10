import pika
import time
#from docker import Client
import subprocess
#from subprocess import Popen, PIPE


class ScaleScanner:

    def __init__(self, amqp_url, queue, update_interval, swarm=True):
        self._url= amqp_url
        self._queue=queue
        self.update_interval = update_interval
        self._swarm_mode=swarm
        #self.cli = Client(base_url='unix://var/run/docker.sock')

    def run_loop(self, service):
        while(True):
            time.sleep(self.update_interval)
            # count the message in the queue
            count_msg = self.count_queue_msg()
            print(str(count_msg)+ ": number of msgs in the queue")
            scale = 1
            if count_msg < 100:
                scale = 5
            elif count_msg < 500:
                scale = 10
            elif count_msg < 1000:
                scale = 30
            else:
                scale = 40

            self.scale_service(service, scale)
            print("Scaled to "+ service + "="+str(scale))


    def scale_service(self, service, scale):
        if(self._swarm_mode):
            self.scale_swarm(service, scale)
        else:
            self.scale_compose(service, scale)


    def scale_compose(self, service_name, scale):

        r = subprocess.run(["docker-compose scale "+ service_name+"="+str(scale)],
        #"docker-compose", "scale",  service_name+"="+str(scale) ],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        print(r.stderr.decode("utf-8"))

    def scale_swarm(self, service_name, scale):

        r = subprocess.run(["docker", "service", "scale",  service_name+"="+str(scale)],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        print(r)

    def count_queue_msg(self):
        #docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dockerfinder_rabbitmq_1
        rabbit_container_name = 'dockerfinder_rabbitmq_1'
        nmap_out = subprocess.run(['docker inspect --format "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" '+ rabbit_container_name],
        #"docker", "inspect", "--format", '"{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}"', "dockerfinder_rabbitmq_1"],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
        ip_rabbit  = nmap_out.stdout.decode("utf-8").rstrip()

        #print("ip rabbit "+str(ip_rabbit)
        url = "amqp://guest:guest@"+ip_rabbit+":5672"
        print("connecting to : " +url)
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
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

    scaling = ScaleScanner('amqp://guest:guest@127.0.0.1:5672','images', 3, swarm=False)  # rabbitmq

    # #while(True):
    # ci = scaling.count_queue_msg()
    # print(str(ci)+ " messages in the rabbitMQ")
    #
    #
    # #scaling.scale_swarm("scanner", 5)
    # scaling.scale_compose("scanner", 2)

    while True:
        try:
            scaling.run_loop("scanner")
        except Exception as e:
            print (e)
            print("In work loop:")
            print("Waiting 10s and restarting.")
            time.sleep(10)


    #update_service with mode={'Replicated': {'Replicas': n}}.
