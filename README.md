# Distance-vector-routing-protocol
Implementation  of distance-vector routing protocol using Bellman-Ford routing algorithm in python. This implementation uses Google's protobufs to communicate between the routers. The neighbours and cost of paths between the routers can be set in text files as provided in config folder.

## Prerequisites
* Python
* Protocol Buffers

## Usage
```bash
python DVR.py [router-id] [any-unique-port-no] [path-to-router-config-file]
```

