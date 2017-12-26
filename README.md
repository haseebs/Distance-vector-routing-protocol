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
## Description
### Config Files
The topology is built using router data from the configfiles. Each router has a configfile which contains the data in format:
```
number_of_neighbours
neighbour_1_cost neighbour_1_port
neighbour_2_cost neighbour_2_port
```
Where the port is used by the neighbour to recieve the distance vector update packets over a UDP connection.


### Distance vector update packet format
The update information is encoded using Protocol Buffers. Each update packet contains the information in format as: 
```
String source_id
Array Neighbours
```
Where each Neighbour is defined as:
```
string neighbour_id
float cost
```

### Process
Upon  initialization, each router creates a distance vector update packet and sends this packet to all direct neighbors. Upon  receiving  this distance vector update packet, each  neighbour incorporates the information into its  routing table. Each router  periodically broadcasts the distance vector update packet to its neighbors every set number of seconds.

Upon recieving the distance vector update packet from the neighbours, each router builds up a reachability matrix. Using this matrix, each router can execute Bellman-Ford algorithm to calculate the least-cost paths to its neighbouring routers. Whenever a path or the cost of a path is changed, distance vector update packet is created again and sent to all the neighbouring routers. This processes keeps going until all the routers converge to least-cost paths.

If at any time during or after this process, a link cost is changed or a path is made unavailable, the change is accomodated as the change is noticed by some router due to timeout (in case it is made unavailable) and notified to all the neighbours through updates until the entire network converges again.
