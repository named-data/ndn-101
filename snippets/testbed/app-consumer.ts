import { connectToNetwork } from "@ndn/autoconfig";
import { consume } from "@ndn/endpoint";
import { Interest } from "@ndn/packet";

// Connect the default forwarder instance to the closest NDN testbed node using the FCH service
await connectToNetwork({
    fallback: ["titan.cs.memphis.edu"],  // optional fallback list
    connectTimeout: 3000,                // optional connection timeout
});

// Send an Interest to a ping server on the testbed
const interest = new Interest(`/ndn/edu/memphis/ping/1234`);
const data = await consume(interest); // wait for echo
