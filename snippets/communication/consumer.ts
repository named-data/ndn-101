import { Interest } from '@ndn/packet';
import { WsTransport } from '@ndn/ws-transport';
import { consume } from '@ndn/endpoint';

// Code running in the browser cannot connect to a local Unix socket.
// In this example, we connect to a remote NFD instance, running as
// a part of the global NDN testbed.
const uplink = await WsTransport.createFace({}, "wss://suns.cs.ucla.edu/ws/");
console.log(`Connected to NFD at ${uplink.remoteAddress}`);

// Create an Interest packet
const interest = new Interest(`/ndn/edu/arizona/ping/NDNts/${Date.now()}`);

// Send the Interest packet and wait for the Data packet
try {
    const data = await consume(interest);
    console.log(`Received data with name [${data.name}]`);
} catch (err: any) {
    console.warn(err);
}

// Disconnect from the remote NFD instance
uplink.close();
