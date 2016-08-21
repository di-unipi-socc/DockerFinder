from subprocess import Popen, PIPE, STDOUT
import re

# http://blog.bordage.pro/avoid-docker-py/

def kill_and_remove(ctr_name):
    for action in ('kill', 'rm'):
        p = Popen('docker %s %s' % (action, ctr_name), shell=True,
                  stdout=PIPE, stderr=PIPE)
        if p.wait() != 0:
            raise RuntimeError(p.stderr.read())


def execute(repo_name, software, options):

    cmd = ['timeout', '-s', 'SIGKILL', '2',
           'docker', 'run', '--rm', repo_name, 'bash', '-c' , software+" " +options]
    # cmd = ['docker', 'run', '--rm','dofinder/softwaretests', 'bash', '-c', 'cat', '/etc/*release'#]
    p = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    out = p.stdout.read().decode()
    return out


if __name__=="__main__":
    # cat / etc / * release
    # 'bash -c"cat /etc/*release"'
    output = execute("dofinder/softwaretests", "python", "--version") #  "-c", "cat", "/etc/*release")
    # print(output)
    p = re.compile('[0-9]*[.][0-9]*[.0-9]*')
    match = p.search(output)
    if match:
        version = match.group(0)
        print("VERAION"+version)