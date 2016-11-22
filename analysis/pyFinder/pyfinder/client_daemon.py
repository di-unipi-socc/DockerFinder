import os
from os import path

import requests.exceptions
from docker import Client, errors

# from . import utility
# from .nodes import Container, Volume
# from .utility import Logger


class Docker_interface:

    def __init__(self, net_name='tosker_net', tmp_dir='/tmp',
                 socket='unix://var/run/docker.sock'):
        self._log = Logger.get(__name__)
        self._net_name = net_name
        self._cli = Client(base_url=os.environ.get('DOCKER_HOST') or socket)
        self._tmp_dir = tmp_dir

    # TODO: aggiungere un parametro per eliminare i container se esistono gia'!
    def create(self, con, cmd=None, entrypoint=None, saved_image=False):
        def create_container():
            tmp_dir = path.join(self._tmp_dir, con.name)
            try:
                os.makedirs(tmp_dir)
            except:
                pass
            saved_img_name = '{}/{}'.format(self._net_name, con.name)
            img_name = con.image
            if saved_image and self.inspect(saved_img_name):
                img_name = saved_img_name

            self._log.debug('container: {}'.format(con.get_str_obj()))

            con.id = self._cli.create_container(
                name=con.name,
                image=img_name,
                entrypoint=entrypoint if entrypoint else con.entrypoint,
                command=cmd if cmd else con.cmd,
                environment=con.env,
                detach=True,
                # stdin_open=True,
                ports=[key for key in con.ports.keys()]
                if con.ports else None,
                volumes=['/tmp/dt'] + ([k for k, v in con.volume.items()]
                                       if con.volume else []),
                networking_config=self._cli.create_networking_config({
                    self._net_name: self._cli.create_endpoint_config(
                        links=con.link
                        # ,aliases=['db']
                    )}),
                host_config=self._cli.create_host_config(
                    port_bindings=con.ports,
                    # links=con.link,
                    binds=[tmp_dir + ':/tmp/dt'] +
                    ([v + ':' + k for k, v in con.volume.items()]
                     if con.volume else []),
                )
            ).get('Id')

        assert isinstance(con, Container)

        if con.to_build:
            self._log.debug('start building..')
            # utility.print_json(
            self._cli.build(
                path='/'.join(con.dockerfile.split('/')[0:-1]),
                dockerfile='./' + con.dockerfile.split('/')[-1],
                tag=con.image,
                pull=True,
                quiet=True
            )
            # )
            self._log.debug('stop building..')
        elif not saved_image:
            # TODO: da evitare se si deve utilizzare un'immagine custom
            self._log.debug('start pulling.. {}'.format(con.image))
            utility.print_json(
                self._cli.pull(con.image, stream=True), self._log.debug)
            self._log.debug('end pulling..')

        try:
            create_container()
        except errors.APIError as e:
            self._log.debug(e)
            # self.stop(con)
            self.delete(con)
            create_container()
            # raise e

    def stop(self, container):
        name = self._get_name(container)
        try:
            return self._cli.stop(name)
        except errors.NotFound as e:
            self._log.error(e)

    def start(self, container, wait=False):
        name = self._get_name(container)
        self._cli.start(name)
        if wait:
            self._log.debug('wait container..')
            self._cli.wait(name)
            utility.print_byte(
                self._cli.logs(name, stream=True),
                self._log.debug
            )

    def delete(self, container):
        name = self._get_name(container)
        try:
            self._cli.remove_container(name, v=True)
        except (errors.NotFound, errors.APIError) as e:
            self._log.error(e)
            raise e

    def exec_cmd(self, container, cmd):
        name = self._get_name(container)
        if not self.is_running(name):
            return False
        try:
            exec_id = self._cli.exec_create(name, cmd)
            status = self._cli.exec_start(exec_id)

            # TODO: verificare attendibilita' di questo check!
            check = 'rpc error:' != status[:10].decode("utf-8")
            self._log.debug('check: {}'.format(check))
            return check
        except errors.APIError as e:
            self._log.error(e)
            return False
        except requests.exceptions.ConnectionError as e:
            # TODO: questo errore arriva dopo un timeout di 10 secodi
            self._log.error(e)
            return False

    def create_volume(self, volume):
        assert isinstance(volume, Volume)
        self._log.debug('volume opt: {}'.format(volume.get_all_opt()))
        return self._cli.create_volume(
            volume.name, volume.driver, volume.get_all_opt()
        )

    def delete_volume(self, volume):
        name = self._get_name(volume)
        return self._cli.remove_volume(name)

    def get_containers(self, all=False):
        return self._cli.containers(all=all)

    def get_volumes(self):
        volumes = self._cli.volumes()
        return volumes['Volumes'] or []

    def inspect(self, item):
        name = self._get_name(item)
        try:
            return self._cli.inspect_container(name)
        except errors.NotFound:
            pass
        try:
            return self._cli.inspect_image(name)
        except errors.NotFound:
            pass
        try:
            return self._cli.inspect_volume(name)
        except errors.NotFound:
            return None

    def remove_all_containers(self):
        for c in self.get_containers(all=True):
            self.stop(c['Id'])
            self.delete(c['Id'])

    def remove_all_volumes(self):
        for v in self.get_volumes():
            self.delete_volume(v['Name'])

    def create_network(self, name, subnet='172.25.0.0/16'):
        # docker network create -d bridge --subnet 172.25.0.0/16 isolated_nw
        # self.delete_network(name)
        try:
            self._cli.create_network(name=name,
                                     driver='bridge',
                                     ipam={'subnet': subnet},
                                     check_duplicate=True)
        except errors.APIError:
            self._log.debug('network already exists!')

    def delete_network(self, name):
        assert isinstance(name, str)
        try:
            self._cli.remove_network(name)
        except errors.APIError:
            self._log.debug('network not exists!')

    def delete_image(self, name):
        assert isinstance(name, str)
        try:
            self._cli.remove_image(name)
        except errors.NotFound:
            pass

    # TODO: splittare questo metodo in due, semantica non chiara!
    def update_container(self, node, cmd, saved_image=True):
        assert isinstance(node, Container)
        # self._log.debug('container_conf: {}'.format(node.host_container))
        stat = self.inspect(node.image)
        old_cmd = stat['Config']['Cmd'] or None
        old_entry = stat['Config']['Entrypoint'] or None

        if self.inspect(node):
            self.stop(node)
            self.delete(node)
        self.create(node, cmd=cmd, entrypoint='', saved_image=saved_image)

        self.start(node.id, wait=True)
        self.stop(node.id)

        name = '{}/{}'.format(self._net_name, node.name)

        self._cli.commit(node.id, name)

        self.stop(node)
        self.delete(node)
        self.create(node,
                    cmd=node.cmd or old_cmd,
                    entrypoint=node.entrypoint or old_entry,
                    saved_image=True)

        self._cli.commit(node.id, name)

    def is_running(self, container):
        name = self._get_name(container)
        stat = self.inspect(name)
        stat = stat is not None and stat['State']['Running'] is True
        self._log.debug('State: {}'.format(stat))
        return stat

    def _get_name(self, name):
        if isinstance(name, six.string_types):
            return name
        else:
            assert isinstance(name, (Container, Volume))
            return name.name
