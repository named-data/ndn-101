# Communication

NDN applications fetch data using Interest-Data packet exchanges. The process of such an exchange can be summarized as follows:

  1. An application that desires a piece of data sends an Interest packet.
     The Interest packet contains the name of the data being requested.
  1. The network forwards the Interest packet to the node(s) having a copy of the data.
  1. On receiving the Interest packet, a node may reply with a matching Data packet.
  1. The network the forwards this Data packet back to the requesting application.

!!! info "Types of Applications"
    Applications that send Interests to fetch data packets are called **"consumers"** <br>
    Likewise, applications that serve Data in response to Interests are called **"producers"** <br>
    An application may act as both a consumer and a producer simultaneously.

## Data Consumer

Consumers are applications that send Interest packets to fetch data. The Interest packet contains the name of the data being requested along with any optional selectors. The following snippet illustrates how to send an Interest packet and get back the corresponding Data.

!!! warning ""
    For this example to work, you must first run the producer from the next part.

=== "ndn-cxx"

    ``` c++
    #include <iostream>
    #include <ndn-cxx/face.hpp>

    int main(int argc, char** argv)
    {
        // Create an Interest packet
        ndn::Interest interest("/edu/ucla/cs/118/notes");

        // Connect to the local forwarder over a Unix socket
        ndn::Face face;

        // Send the Interest packet and get back the Data packet
        face.expressInterest(interest,
                            [](const ndn::Interest&, const ndn::Data& data) {
                                // Received a Data packet reply
                                std::cout << data << std::endl;
                            },
                            [](const ndn::Interest&, const ndn::lp::Nack& nack) {
                                // Received a Nack (negative acknowledgement)
                                std::cout << "Nack received: " << nack.getReason() << std::endl;
                            },
                            [](const ndn::Interest&) {
                                // The Interest has timed out
                                std::cout << "Timeout" << std::endl;
                            });

        // Start face processing loop
        face.processEvents();
    }
    ```

=== "python-ndn"

    ``` python
    from ndn.app import NDNApp
    from ndn.encoding import Name

    # Connect to the local forwarder over a Unix socket
    app = NDNApp()

    async def main():
        try:
            data_name, meta_info, content = await app.express_interest("/edu/ucla/cs/118/notes")

            # Received a Data packet
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(content) if content else None)

        except InterestNack as e:
            # Received a Nack (negative acknowledgement)
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            # The Interest has timed out
            print(f'Timeout')
        except InterestCanceled:
            # Connection to the local NDN forwarder is broken
            print(f'Canceled')
        except ValidationFailure:
            # Security validation failed for the data
            print(f'Data failed to validate')

        finally:
            # Disconnect from the local forwarder
            app.shutdown()

    if __name__ == '__main__':
        app.run_forever(after_start=main())
    ```

=== "NDNts"

    ``` typescript
    import { Interest } from '@ndn/packet';
    import { WsTransport } from '@ndn/ws-transport';
    import { Endpoint } from '@ndn/endpoint';

    // Code running in the browser cannot connect to a local Unix socket.
    // In this example, we connect to a remote NFD instance, running as
    // a part of the global NDN testbed.
    const uplink = await WsTransport.createFace({}, "wss://suns.cs.ucla.edu/ws/");
    console.log(`Connected to NFD at ${uplink.remoteAddress}`);

    // Construct an Endpoint on the default forwarder instance.
    const endpoint = new Endpoint();

    // Create an Interest packet
    const interest = new Interest(`/ndn/edu/arizona/ping/NDNts/${Date.now()}`);

    // Send the Interest packet and wait for the Data packet
    try {
        const data = await endpoint.consume(interest);
        console.log(`Received data with name [${data.name}]`);
    } catch (err: any) {
        console.warn(err);
    }

    // Disconnect from the remote NFD instance
    uplink.close();
    ```

## Data Producer

To serve data to other applications, a producer must register a name prefix with the network.

  1. The producer sends a registration request to the network carrying a name prefix.
  1. A route to the prefix is registered at the local forwarder, and may be propagated to other forwarders in the network.
  1. The producer is notified of the successful registration.
  1. Any Interest packets matching the prefix may now be forwarded to the producer.

The following snippet illustrates how to serve data by registering a name prefix route at the local forwarder.

=== "ndn-cxx"

    ``` c++
    #include <iostream>
    #include <ndn-cxx/face.hpp>
    #include <ndn-cxx/security/key-chain.hpp>

    int main(int argc, char** argv)
    {
        // Connect to the local forwarder over a Unix socket
        ndn::Face face;

        // Connect to the local KeyChain to sign Data packets
        // Note: Security is not optional in NDN
        ndn::KeyChain keychain;

        // Register a prefix with the local forwarder
        face.setInterestFilter("/edu/ucla/cs/118/notes",
            [&face, &keychain](const ndn::InterestFilter&, const ndn::Interest& interest) {
                std::cout << "Received Interest packet for " << interest.getName() << std::endl;

                // Create a Data packet with the same name as the Interest
                ndn::Data data(interest.getName());

                // Set the Data packet's content to "Hello, World!"
                data.setContent(ndn::make_span(reinterpret_cast<const uint8_t*>("Hello, NDN!"), 11));

                // Sign the Data packet with default identity
                keychain.sign(data);

                // Return the Data packet to the network
                face.put(data);
            },

            // Register prefix failure handler -- optional
            nullptr,

            // Register prefix failure handler
            [](const ndn::Name& prefix, const std::string& reason) {
                std::cout << "Route registration failed" << std::endl;
            });

        // Start face processing loop
        face.processEvents();
    }
    ```

=== "python-ndn"

    ``` python
    from typing import Optional
    from ndn.app import NDNApp
    from ndn.encoding import Name, InterestParam, BinaryStr, FormalName

    # Connect to the local forwarder over a Unix socket
    app = NDNApp()

    # Register a prefix, and call on_interest when a matching Interest is received
    @app.route('/edu/ucla/cs/118/notes')
    def on_interest(name: FormalName, param: InterestParam, _app_param: Optional[BinaryStr]):
        print(f'Received Interest packet for {Name.to_str(name)}')

        # Create the content bytes for the Data packet
        content = "Hello, NDN!".encode()

        # Sign and send the Data packet back to the network
        app.put_data(name, content=content, freshness_period=10000)

    if __name__ == '__main__':
        app.run_forever()
    ```
