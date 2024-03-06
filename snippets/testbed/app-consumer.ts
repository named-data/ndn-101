import { connectToNetwork } from "@ndn/autoconfig";
import { Endpoint } from "@ndn/endpoint";
import { Interest } from "@ndn/packet";

// Connect the default forwarder instance to the closest NDN testbed node using the FCH secvice
await connectToNetwork({
    fallback: ["titan.cs.memphis.edu"],  // optional fallback list
    connectTimeout: 3000,                // optional connection timeout
});

// Create an endpoint using the default forwarder instance
const endpoint = new Endpoint();

// Send an Interest to a ping server on the testbed
const interest = new Interest(`/ndn/edu/memphis/ping/1234`);
const data = await endpoint.consume(interest); // wait for echo
