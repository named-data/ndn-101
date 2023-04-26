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