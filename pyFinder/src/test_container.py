import unittest
from  pyDescriptor import Container
import re
import yaml
import os

class TestContainer(unittest.TestCase):

    def test_run_commnads(self):
        #list_commands = ['python --version', 'java  -version', 'perl  -version']
        #command = ['sh', '-c', 'python --version && java  -version && perl  -version']
        repo_name = "java"  # ad ad hoc image
        bins = []
        with Container(repo_name) as c:
            for bin, cmd, regex in self._get_bins("../resources/versions.yml"):
                output = c.run(bin + " " + cmd)
                p = re.compile(regex)
                match = p.search(output)
                if match:
                    version = match.group(0)
                    print("[{0}] found {1}: {2}".format(repo_name, bin, version))
                    bins.append({'bin': bin, 'ver': version})



    def _get_bins(self, yml_cmd_path):
        versionCommands = yaml.load(open(yml_cmd_path)) #os.path.dirname(__file__) +
        apps = versionCommands['applications']
        for app in apps:
            yield app["name"], app["ver"], app["re"]