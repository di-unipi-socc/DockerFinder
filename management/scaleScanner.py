import requests
import time
import subprocess
#from subprocess import Popen, PIPE


class ScaleScanner:

    def __init__(self, update_interval, swarm=True):
        self.update_interval = update_interval
        self._swarm_mode=swarm

        # TODO; change from rabbitmq to monitor service
        self._rabbitUrl = "http://0.0.0.0:3002/service/rabbitmq/queue/images"

    def run_loop(self, service):
        while(True):
            time.sleep(self.update_interval)
            # count the message in the queue
            res = requests.get(self._rabbitUrl)

            if res.status_code == requests.codes.ok:
                json_response = res.json()
                #print(json_response)
                if(not json_response['err']):
                    count_msg=json_response['load']
                    print(str(count_msg)+  ": msgs in the queue")
                    scale = 1
                    if count_msg < 100:
                        scale = 5
                    elif count_msg < 500:
                        scale = 10
                    elif count_msg < 1000:
                        scale = 30
                    else:
                        scale = 40
                    #scale the scanners
                    self.scale_service(service, scale)
                else:
                    print(json_response['msg'])

    def scale_service(self, service, scale):
        if(self._swarm_mode):
            self.scale_swarm(service, scale)
        else:
            self.scale_compose(service, scale)


    def scale_compose(self, service_name, scale):

        command = "docker-compose scale "+ service_name+"="+str(scale)
        print("Scaling compose mode :"+ command)
        #r =    subprocess.check_output(["docker-compose scale "+ service_name+"="+str(scale)],
        r = subprocess.call(command, shell=True)
        #r = subprocess.run(["docker-compose scale "+ service_name+"="+str(scale)],
        #"docker-compose", "scale",  service_name+"="+str(scale) ],
        #                shell=True,
        #                stdout=subprocess.PIPE,
        #                stderr=subprocess.PIPE)
        #print(r.stderr.decode("utf-8"))

    def scale_swarm(self, service_name, scale):
        command = "docker service scale "+service_name+"="+str(scale)
        print("Scaling swarm mode: "+ command)
        r = subprocess.call(command, shell=True)
        # r = subprocess.run(["docker", "service", "scale",  service_name+"="+str(scale)],
        #                 shell=True,
        #                 stdout=subprocess.PIPE,
        #                 stderr=subprocess.PIPE)
        #print(r)


if __name__ == '__main__':

    scaling = ScaleScanner(5, swarm=False)  # rabbitmq

    while True:
        try:
            scaling.run_loop("scanner")
        except Exception as e:
            print (e)
            print("Waiting 10s and restarting.")
            time.sleep(10)


    #update_service with mode={'Replicated': {'Replicas': n}}.
