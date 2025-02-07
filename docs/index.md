---
title: Introduction
---

# Introduction to Named Data Networking

Named Data Networking (NDN)[@sigcomm2014ndn] is a future Internet architecture inspired by years of research into network usage and a growing awareness of unsolved problems in the contemporary protocols. Many of these problems arise due to the fundamental mismatch between the data-centric usage of the Internet and the host-centric nature of IP. NDN is designed as a data-centric replacement of the TCP/IP architecture, thus overcoming this mismatch by replacing the network layer itself. The NDN project is now a collaborative effort of a large community of researchers at more than a dozen institutions.

NDN retains the Internet's hourglass architecture but evolves the thin waist to allow the creation of completely general distribution networks. The core element of this evolution is removing the restriction that packets can only identify communication endpoints. As far as the network is concerned, the identifier in an NDN packet can be anything — an endpoint, a chunk of movie or book, a command to turn on some lights, etc. This conceptually simple change allows NDN networks to use almost all of the Internet’s well understood and well tested engineering properties to efficiently solve not only communication problems but also digital distribution and control problems.

!!! info "A more detailed discussion can be found at the website of the NDN project ([named-data.net](https://named-data.net))"

The design of NDN naturally leads to several advantages over IP and IP-based protocols. Some of these are briefly described below.

 - **Data-Centric Security**: NDN provides data-centric security[@ieeecomm2018security] where it secures data directly rather than relying on securing the channels that transmit the data. Each packet of data carries a cryptographic signature that binds the name, contents and the identity of the producer of the data.

 - **Privacy**: NDN provides privacy by allowing consumers to retrieve data without needing to expose their identity to the network. This is in contrast to IP where the source and destination addresses are exposed in every packet.

 - **Name-based Forwarding**: NDN packets are routed and forwarded using their names. This allows NDN routers to make forwarding decisions based on application semantics rather than just network addresses. This also directly provides support for anycast for applications.

 - **Intelligent Data Plane**: NDN utilizes a stateful forwarding plane where forwarders track the requests and responses of data. This allows NDN to support a wide range of advanced features such as adaptive and multipath forwarding, and provides DDoS protection[@icccn2013ddos] and congestion control[@icn2019congestion] at the network layer.

 - **Multicast and Caching**: The stateful forwarding plane allows for aggregation of requests and responses, which enables efficient multicast of all Data packets. Since NDN packets are individually secured and do not rely on channel security, data is also securely cached at every forwarder in the network, creating a massive distributed cache.

The NDN project also maintains a large open source code base, with NDN forwarders, debugging tools and libraries available in multiple languages including C++, Python, Go, TypeScript etc. Most of this code is available at [GitHub](https://github.com/named-data).
