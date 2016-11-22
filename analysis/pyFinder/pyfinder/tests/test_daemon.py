import unittest
import docker
from pyfinder import Container
import re

class TestDaemon(unittest.TestCase):

    def setUp(self):
        self.client = docker.Client(base_url='unix://var/run/docker.sock')
        #client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname=False))

    def test_run(self):
        repo_name = "python"  # ad ad hoc image
        bins = []
        with Container(repo_name) as c:
            for bin, cmd, regex in self.gen_bins():
                output = c.run(bin + " " + cmd)
                p = re.compile(regex)
                match = p.search(output)
                if match:
                    version = match.group(0)
                    print("[{0}] found {1}: {2}".format(repo_name, bin, version))
                    bins.append({'bin': bin, 'ver': version})
        self.assertGreater(len(bin), 0)

    def gen_bins(self):
        d =(("python", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
            ("python3", "--version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
            ("python2", "--version",  '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
            ("java", "-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
            ("curl","--version",'[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'),
            ("nano","-version", '[0-9]*\.[0-9]*[a-zA-Z0-9_\.-]*'))
        for list in d:
            yield list[0], list[1],list[2]


if __name__ == '__main__':
    unittest.main()
