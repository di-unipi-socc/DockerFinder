from pyDescriptor import Scanner

if __name__ == "__main__":
    s = Scanner(host_rabbit='172.17.0.3', host_api="127.0.0.1", port_api=8000)
    s.run()