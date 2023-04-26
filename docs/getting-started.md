# Getting Started

This page will guide you through the process of installing the basic tools needed to start using and developing NDN applications.

To begin, you will need to first install the **NDN Forwarding Daemon (NFD)** on your computer.
There are several implementations of NFD, the most popular of which are:

  * [NFD](https://docs.named-data.net/NFD/current/INSTALL.html), the reference implementation (C++)
  * [YaNFD](https://github.com/named-data/yanfd), a multithreaded implementation (Golang)
  * [NDN-DPDK](https://github.com/usnistgov/ndn-dpdk), a high-performance implementation (C)
  * [NDN-Lite](https://github.com/named-data-iot/ndn-lite), an IoT implementation (C)

!!! tip "What is the role of NFD?"
    NFD is the NDN equivalent of an IP "router", and runs on _each node_ in the network.
    It is responsible for forwarding NDN packets between nodes, including functions of Data multicast and caching.

Next, you will need to install a **client library** of your choice to interact with the NDN network.
Depending on the library, you will need the corresponding compilers / interpreters / build tools.

  * [ndn-cxx](https://github.com/named-data/ndn-cxx), reference implementation (C++)
  * [python-ndn](https://github.com/named-data/python-ndn) (Python)
  * [NDNts](https://github.com/yoursunny/NDNts) (TypeScript)
  * [go-ndn](https://github.com/zjkmxy/go-ndn) (Golang)
  * [NDN-Lite](https://github.com/named-data-iot/ndn-lite), an IoT implementation (C)
  * [esp8266ndn](https://github.com/yoursunny/esp8266ndn) (Arduino)

!!! tip "What does the client library do?"

    The client library provides the NDN equivalent of a TCP/IP "socket", and runs inside _each application_.
    It is responsible for encoding and decoding NDN packets, and sending / receiving them to / from NFD.

Once you have installed NFD and a client library, you need to start NFD on your local development machine.
You are now ready to start developing NDN applications!