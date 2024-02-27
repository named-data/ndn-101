import { Data, digestSigning } from '@ndn/packet';
import { WsTransport } from '@ndn/ws-transport';
import { Endpoint } from '@ndn/endpoint';
import { toUtf8 } from '@ndn/util';

// Code running in the browser cannot connect to a local Unix socket.
// In this example, we connect to a remote NFD instance, running as
// a part of the global NDN testbed.
const uplink = await WsTransport.createFace({}, "wss://suns.cs.ucla.edu/ws/");
console.log(`Connected to NFD at ${uplink.remoteAddress}`);

// Construct an Endpoint on the default forwarder instance.
const endpoint = new Endpoint();

// Start one producer
const myProducer = endpoint.produce('/edu/ucla/cs/118/notes', async (interest) => {
    console.log(`Received Interest packet for ${interest.name.toString()}`);
    // Create the content bytes for the Data packet
    const content = toUtf8("Hello, NDN!");
    // Sign and send the Data packet back to the network
    const data = new Data(interest.name, Data.FreshnessPeriod(10000), content);
    await digestSigning.sign(data);
    return data;
});
