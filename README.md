# Distance-vector-routing-protocol
Implementation  of distance-vector routing protocol using Bellman-Ford algorithm in python. This implementation uses Google's protobufs to communicate between the routers. The neighbours and cost of paths between the routers can be set in text files as provided in config folder.

## Prerequisites
* Python
* Protocol Buffers
* Tmux and Tmuxinator [Both Optional, for starting multiple routers at once]

## Usage
For starting multiple routers at once (Recommended):
* Modify the [root] attribute in nodes.yml to point to where the project was cloned
* Place the nodes.yml in ~/.tmuxinator/nodes.yml
* cd to root of the project folder
* Execute ```tmuxinator start nodes ```

For starting a router manually:
```bash
python DVR.py [router-id] [any-unique-port-no] [path-to-router-config-file]
```

