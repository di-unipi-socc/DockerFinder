
## FastFlow + Docker
We are investigating the possibility to execute FastFlow programs within the Docker platform.

The goal is to test:
- **elasticity**:  the resources (CPU , Memory) needed by FF program executed in a Docker container can be dynamically allocated (e.g. increasing the cores needed by a FF program, changing the graph topology- increasing the workers in a farm)
- **multi-tenant**: two programs running on the same host should not interfere with each others.

### Thread-affinity in Docker
Docker is able to guarantee *thread-affinity* in order to authorize a given application to access only some CPUs ( via `--cpuset-cpus` command)

The test uses the image `agileek/cpuset-test` that it is configured to run the [cpuburn](https://patrickmn.com/projects/cpuburn/) script for load the CPUs of a machine.

Starts the container with name `test` assigning only the CPU 0.

`docker run -ti --cpuset-cpus=0 --name test agileek/cpuset-test`

With the `update` command it is possible to change the number of CPUs at runtime.

`docker update --cpuset-cpus=0,2 test`



IN order to test if a container detects the CPUs also with the `--cpuset-cpus` flag.

`docker run -ti --cpuset-cpus=2 ubuntu grep proc cat /proc/cpuinfo`


### Conclusion
1. *elasticity*: (resolved) with the `update` command and the `--cpuset-cpus` option the resources (e.g. number of CPUs) of a FF program executing in a Docker container can be dynamically allocated.
2. *multi-tenant*:(resolved) two FF programs can be executed in two Docker containers mapping only onto subset of CPUs.


## Update options
<table>
  <thead>
    <tr>
      <th>Name, shorthand</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code class="highlighter-rouge">--blkio-weight</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpu-period</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>Limit CPU CFS (Completely Fair Scheduler) period</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpu-quota</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>Limit CPU CFS (Completely Fair Scheduler) quota</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpu-rt-period</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>Limit the CPU real-time period in microseconds</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpu-rt-runtime</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>Limit the CPU real-time runtime in microseconds</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpu-shares, -c</code></td>
      <td><code class="highlighter-rouge">0</code></td>
      <td>CPU shares (relative weight)</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpuset-cpus</code></td>
      <td>&nbsp;</td>
      <td>CPUs in which to allow execution (0-3, 0,1)</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--cpuset-mems</code></td>
      <td>&nbsp;</td>
      <td>MEMs in which to allow execution (0-3, 0,1)</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--kernel-memory</code></td>
      <td>&nbsp;</td>
      <td>Kernel memory limit</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--memory, -m</code></td>
      <td>&nbsp;</td>
      <td>Memory limit</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--memory-reservation</code></td>
      <td>&nbsp;</td>
      <td>Memory soft limit</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--memory-swap</code></td>
      <td>&nbsp;</td>
      <td>Swap limit equal to memory plus swap: ‘-1’ to enable unlimited swap</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">--restart</code></td>
      <td>&nbsp;</td>
      <td>Restart policy to apply when a container exits</td>
    </tr>
  </tbody>
</table>
