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