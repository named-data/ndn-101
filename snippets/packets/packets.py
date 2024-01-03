import ndn.encoding as enc
import ndn.security as sec

#  Create an Interest packet with its NDN name from a URI string
interest_wire = enc.make_interest(
    enc.Name.from_str('/edu/ucla/cs/118/notes'),
    # Set the Interest packet's InterestLifetime to 5 seconds
    enc.InterestParam(lifetime=5000),
)
print(interest_wire.hex())
# In python-ndn you do not have to encode the Interest manually.
# NDNApp's express function provides a more flexible API to send an Interest directly.

# Create a SHA256 digest signer
digest_signer = sec.DigestSha256Signer()
# Create a Data packet with the same name
data_wire = enc.make_data(
    # String can be directly used as Name in most cases
    name='/edu/ucla/cs/118/notes',
    # Set the Interest packet's FreshnessPeriod to 10 seconds
    meta_info=enc.MetaInfo(freshness_period=10000),
    # Set the Data packet's content to "Hello, NDN!"
    content=b'Hello, NDN!',
    signer=digest_signer
)
print(data_wire.hex())
