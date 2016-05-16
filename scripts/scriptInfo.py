import platform
import sys

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

dictInfo = dict()

dictInfo['Linux_dist'] = linux_distribution()
dictInfo['system']=platform.system()
dictInfo['platform'] = platform.system()
dictInfo['pyVer'] = sys.version.split('\n')
