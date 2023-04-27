# Communication

NDN applications fetch data using Interest-Data packet exchanges. The process of such an exchange can be summarized as follows:

  1. An application that desires a piece of data sends an Interest packet.
     The Interest packet contains the name of the data being requested.
  1. The network forwards the Interest packet to the node(s) having a copy of the data.
  1. On receiving the Interest packet, a node may reply with a matching Data packet.
  1. The network the forwards this Data packet back to the requesting application.

!!! info "Types of Applications"
    Applications that send Interests to fetch data packets are called **"consumers"**.
    Likewise, applications that serve Data in response to Interests are called **"producers"**.
    An application may act as both a consumer and a producer simultaneously.

## Data Consumer

Consumers are applications that send Interest packets to fetch data. The Interest packet contains the name of the data being requested along with any optional selectors. The following snippet illustrates how to send an Interest packet and get back the corresponding Data.

!!! warning ""
    For this example to work, you must first run the producer from the next part.

=== "ndn-cxx"

    ``` c++
    --8<-- "snippets/communication/consumer.cpp"
    ```

=== "python-ndn"

    ``` python
    --8<-- "snippets/communication/consumer.py"
    ```

=== "NDNts"

    ``` typescript
    --8<-- "snippets/communication/consumer.ts"
    ```

## Data Producer

To serve data to other applications, a producer must register a name prefix with the network.

  1. The producer sends a registration request to the network carrying a name prefix.
  1. A route to the prefix is registered at the local forwarder, and may be propagated to other forwarders in the network.
  1. The producer is notified of the successful registration.
  1. Any Interest packets matching the prefix may now be forwarded to the producer.

The following snippet illustrates how to serve data by registering a name prefix route at the local forwarder.
Make sure to start NFD on your development machine before running this example.

=== "ndn-cxx"

    ``` c++
    --8<-- "snippets/communication/producer.cpp"
    ```

=== "python-ndn"

    ``` python
    --8<-- "snippets/communication/producer.py"
    ```

## Faces

!!! warning "Under Construction"
