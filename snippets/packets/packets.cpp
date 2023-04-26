#include <ndn-cxx/face.hpp>

int main(int argc, char** argv)
{
    // Create an NDN Name from a URI string
    ndn::Name name("/edu/ucla/cs/118/notes");

    // Create an Interest packet with this name
    ndn::Interest interest(name);

    // Set the Interest packet's InterestLifetime to 5 seconds
    interest.setInterestLifetime(ndn::time::seconds(5));

    // Create a Data packet with the same name
    ndn::Data data(name);

    // Set the Data packet's content to "Hello, NDN!"
    data.setContent(ndn::make_span(reinterpret_cast<const uint8_t*>("Hello, NDN!"), 11));
}