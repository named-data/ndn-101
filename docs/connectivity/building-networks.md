---
title: Building Networks
---

# Building NDN Networks

Before running NDN applications, you may need to set up your own NDN network or connect to the existing global NDN testbed. This section describes the process of building your own network. A more detailed example for NDNd suitable for beginners can be found [here](https://github.com/named-data/ndnd/blob/main/docs/daemon-example.md).

NDN applications interact with the network using an general purpose abstraction called faces. A face may, for instance, be backed an actual ethernet interface or it tunnel over a UDP or TCP connection. NDN forwarders, in turn, also connect to each other over faces, which may be either tunnels or physical links. Thus, building an NDN network consists of two steps:

1. Configuring faces at each forwarder to each neighbor of that forwarder. This step is equivalent to physically plugging in cables on a traditional IP router.
2. Configuring routes to data prefixes between forwarders. This step can be done either manually or using a routing protocol.

The example below shows how to manually create an NDN face over a UDP tunnel between two NDN forwarders using the nfdc and NDNd CLI tools. Both nodes must already be running an NDN forwarder before this step.

=== "ndn-cxx"

    ```bash
    # https://docs.named-data.net/NFD/24.07/manpages/nfdc-face.html
    nfdc face create remote udp://router.example.net
    ```

=== "NDNd"

    ```bash
    # https://github.com/named-data/ndnd/blob/main/docs/fw-control.md
    ndnd fw face-create remote=udp://router.example.net
    ```


Once a face is created, you can use the same tool to add routes between the two forwarders and start transferring data.

=== "ndn-cxx"

    ```bash
    # Add route for /example to remote
    # https://docs.named-data.net/NFD/24.07/manpages/nfdc-route.html
    nfdc route add prefix /example nexthop udp://router.example.net
    ```

=== "NDNd"

    ```bash
    # Add route for /example to remote
    # https://github.com/named-data/ndnd/blob/main/docs/fw-control.md
    ndnd fw route-add prefix=/example face=udp://router.example.net
    ```

You can now start an NDN ping server on the example forwarder and the prefix would be reachable from the router creating the face.

=== "ndn-cxx"

    ```bash
    # Run on the "router.example.net" node
    ndnpingserver /example/server

    # Run on the first node
    ndn ping /example/server
    ```

=== "NDNd"

    ```bash
    # Run on the "router.example.net" node
    ndnd pingserver /example/server

    # Run on the first node
    ndnd ping /example/server
    ```