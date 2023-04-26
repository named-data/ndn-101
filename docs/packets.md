# Packet Types

At a high level, NDN defines two distinct types of packets:

  * **Interest** packets are used to _request data_ from the network. The most important component of an Interest packet is the _name_ of the data being requested. An Interest may contain additional parameters such as a _lifetime_ or _hop limit_, which are referred to as selectors.
  * **Data** packets carry the _actual data_ being requested, along with the name of the Data and a cryptographic signature. On receiving an Interest packet, nodes in the network may respond with a Data matching the name in the Interest.

!!! tip "How are NDN packets used?"
    Interest and Data packets are used in a **request-response** fashion. An NDN application sends an Interest packet to request data from the network, and receives a single Data packet in response.

The following example illustrates the basic structure of Interest and Data packets.

``` mermaid
classDiagram
  Interest <|-- Data
  class Interest{
    Name = /edu/ucla/cs/118/notes
    Lifetime = 5000 ms
  }
  class Data{
    Name = /edu/ucla/cs/118/notes
    Content = "Hello, NDN!"
    Signature = 3046022100e773b
  }
```

!!! tip "`CanBePrefix` Interest Selector"
    In this example, the name of the Interest and Data packets is an exact match. If the `CanBePrefix` selector is specified on the Interest, the name of a matching Data packet may be longer than the name of the Interest packet, as long as it has the name of the Interest as a prefix.

!!! warning "Data Signing"
    It is important to note that a Data packet is **required** to carry a signature to be considered valid.

## TLV Encoding

On the wire, NDN packets are represented using the Type-Length-Value ([NDN TLV](https://docs.named-data.net/NDN-packet-spec/current/tlv.html#ndn-tlv-encoding)) encoding scheme. TLV is a highly efficient binary encoding scheme that supports variable length fields and nested structures.

Each field in the packet is encoded as a TLV element, which consists of a **type**, **length**, and **value**. The type and length fields are encoded as variable length integers, and the value field is encoded as a sequence of bytes (which in turn may be another TLV block). Interest and Data packets themselves are also encoded as TLV elements.

The following example illustrates the TLV encoding of the Interest and Data packets shown above. The type of the block is specified first (in red, hover for numeric), followed by the length (in blue) and the value.

<div>
    <iframe
        src="https://play.ndn.today/?visualize=0527071b0803656475080475636c6108026373080331313808056e6f7465730a048ddbcef10c021388"
        crossorigin="anonymous" data-message-fun="handleVisMessage" style="border: none; width: 100%; margin-bottom: 10px">
    </iframe>
    <iframe
        src="https://play.ndn.today/?visualize=06A2071B0803656475080475636C6108026373080331313808056E6F746573150B48656C6C6F2C204E444E21162C1B01031C2707250803656475080475636C610802637308056C6978696108034B455938080005FA3ADE0C75D817483046022100E773B365BE4FCED756073E9183A46258206F1624BC04B55ABE41CA4E259FBCF3022100D8F5CDCF0C946D71142708AABDC18819B4E9C6990DEC90AE0306E1A7E7D663C6"
        crossorigin="anonymous" data-message-fun="handleVisMessage" style="border: none; width: 100%">
    </iframe>

</div>

!!! tip "Encoding of Names"
    NDN names are hierarchical and are encoded as a list of components. Each component is treated as an opaque binary value by the network, and may contain any sequence of bytes with no restrictions. For readability, names may be represented using the [NDN URI Scheme](https://docs.named-data.net/NDN-packet-spec/current/name.html#ndn-uri-scheme) using slashes as delimiters between components.

!!! info "Packet Format Specification"
    The formal specification for Interest and Data packets and TLV encoding can be accessed [here](https://docs.named-data.net/NDN-packet-spec/current/).

## Library Functions

This section describes how to encode Interest and Data packets using some of the NDN client libraries.
The next page will describe how to use the libraries to send and receive the packets.

=== "ndn-cxx"

    ``` c++
    --8<-- "snippets/packets/packets.cpp"
    ```

=== "python-ndn"

    ``` python
    --8<-- "snippets/packets/packets.py"
    ```

=== "NDNts"

    ``` typescript
    --8<-- "snippets/packets/packets.ts"
    ```