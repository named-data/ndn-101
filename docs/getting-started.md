---
title: Getting Started
---

# Getting Started with NDN

This page will guide you through the process of installing the basic tools needed to start using and developing NDN applications.

## Packet Forwarder

To begin, you will need to first install an **NDN Packet Forwarder** on your computer.
There are several implementations of forwarders, the most popular of which are:

  * [NFD](https://docs.named-data.net/NFD/current/INSTALL.html)[@afanasyev2014nfd], the reference implementation (C++)
  * [NDNd](https://github.com/named-data/ndnd)[@icn2021yanfd], a multithreaded implementation (Golang)
  * [NDN-DPDK](https://github.com/usnistgov/ndn-dpdk)[@icn2020dpdk], a high-performance implementation (C)
  * [NDN-Lite](https://github.com/named-data-iot/ndn-lite)[@icn2018ndnot], an IoT implementation (C)

!!! tip "What is the role of the forwarder?"
    The forwarder is the NDN equivalent of an IP "router", and runs on _each node_ in the network.
    It is responsible for forwarding NDN packets between nodes, including functions of Data multicast and caching.

## Client Library

Next, you will need to install a **client library** of your choice to interact with the NDN network.
Depending on the library, you will need the corresponding compilers / interpreters / build tools.

  * [ndn-cxx](https://github.com/named-data/ndn-cxx) (C++) [[Docs](https://docs.named-data.net/ndn-cxx/current/INSTALL.html), [API](https://docs.named-data.net/ndn-cxx/current/doxygen/annotated.html)]
  * [NDNd](https://github.com/named-data/ndnd) (Golang) [[API](https://pkg.go.dev/github.com/named-data/ndnd)]
  * [python-ndn](https://github.com/named-data/python-ndn) (Python) [[Docs](https://python-ndn.readthedocs.io/en/latest/)]
  * [NDNts](https://github.com/yoursunny/NDNts) (TypeScript) [[Docs](https://yoursunny.com/p/NDNts/)]
  * [NDN-Lite](https://github.com/named-data-iot/ndn-lite) (C, IoT) [[Docs](https://github.com/named-data-iot/ndn-lite/wiki), [API](https://zjkmxy.github.io/ndn-lite-docs/index.html)]
  * [esp8266ndn](https://github.com/yoursunny/esp8266ndn) (Arduino) [[API](https://esp8266ndn.ndn.today/)]

!!! tip "What does the client library do?"

    The client library provides the NDN equivalent of a TCP/IP "socket", and runs inside _each application_.
    It is responsible for encoding and decoding NDN packets, and sending / receiving them to / from NFD.

Once you have installed NFD and a client library, you need to start NFD on your local development machine.
You are now ready to start developing NDN applications!

!!! info "Contributing to the NDN codebase"

    The NDN codebase is free and open-source software, and most of it is available on [GitHub](https://github.com/named-data). If you are interested in contributing, make sure you read [this guide](https://github.com/named-data/.github/blob/main/CONTRIBUTING.md) and the [code of conduct](https://github.com/named-data/.github/blob/main/CODE_OF_CONDUCT.md) first.

## Debugging Tools

The [ndn-tools](https://github.com/named-data/ndn-tools) package is highly recommended and contains several tools for developing and debugging NDN applications. The [NDNd](https://github.com/named-data/ndnd) package also offers many of these tools with prebuilt binaries available.

  * [peek](https://github.com/named-data/ndn-tools/blob/master/tools/peek/README.md): transmit a single Interest/Data packet between a consumer and a producer.
  * [get](https://github.com/named-data/ndn-tools/blob/master/tools/get/README.md) and [serve](https://github.com/named-data/ndn-tools/blob/master/tools/serve/README.md): segmented file transfer between a consumer and a producer.
  * [ping](https://github.com/named-data/ndn-tools/blob/master/tools/ping/README.md): test reachability between two NDN nodes
  * [dump](https://github.com/named-data/ndn-tools/blob/master/tools/dump/README.md): capture and analyze live traffic on an NDN network
  * [dissect](https://github.com/named-data/ndn-tools/blob/master/tools/dissect/README.md): inspect the TLV structure of an NDN packet
  * [dissect-wireshark](https://github.com/named-data/ndn-tools/blob/master/tools/dissect-wireshark/README.md): Wireshark extension to inspect the TLV structure of NDN packets

!!! tip "Ping test"

    You can run a simple test for your local NDN forwarder by using the ndn-tools or NDNd packages to start a ping server and client on the same machine. These will then communicate by connecting to the forwarder over a unix socket.

    === "ndn-tools"

        ```bash
        ndnpingserver /my/nfd/test &
        ndnping /my/nfd/test
        ```

    === "NDNd"

        ```bash
        ndnd pingserver /my/ndnd/test &
        ndnd ping /my/ndnd/test
        ```

## Getting Help

If you have any questions about NDN or the code base, we encourage you to reach out to the community for help.
Some options include,

  - Ask a question at the most appropriate [mailing list](https://named-data.net/codebase/platform/support/mailing-lists/).
  - File an issue at the relevant [GitHub](https://github.com/named-data) repository or [Redmine](https://redmine.named-data.net/projects).
  - (If applicable) reach out to the authors of the paper that introduced the software.
