#include <cassert>
#include <ndn-cxx/ims/in-memory-storage-persistent.hpp>
#include <ndn-cxx/security/key-chain.hpp>

int main(int argc, char** argv)
{
    // Create an in-memory application-specific storage
    ndn::InMemoryStoragePersistent ims;

    // Create and sign a data packet
    auto data = std::make_shared<ndn::Data>("/test/data");
    data->setContent("Hello, World!");
    ndn::KeyChain keyChain;
    keyChain.sign(*data);

    // Insert a data packet into the store
    ims.insert(*data);

    // Find a data packet in the store
    ndn::Interest interest("/test/data");
    assert(ims.find(interest)->getName() == data->getName());
}
