import ndn.encoding as enc
import ndn.security as sec
from Cryptodome.PublicKey import ECC

# Generate key pairs (Recommend 'P-256' for ECDSA and 'ed25519' for EdDSA)
priv_key = ECC.generate(curve='ed25519')
pub_key = priv_key.public_key()
# Create a signer
signer = sec.Ed25519Signer('/edu/ucla/xinyu.ma', priv_key.export_key(format='DER'))
# Sign a data with it
data_wire = enc.make_data(
    # String can be directly used as Name in most cases
    name='/edu/ucla/cs/118/notes',
    # Set the Interest packet's FreshnessPeriod to 10 seconds
    meta_info=enc.MetaInfo(freshness_period=10000),
    # Set the Data packet's content to "Hello, NDN!"
    content=b'Hello, NDN!',
    signer=signer
)
print('Data:', data_wire.hex())

# Export public keys
pub_key_bits = pub_key.export_key(format='DER')
print('Public Key bits:', pub_key_bits.hex())
# Can be imported by: ECC.import_key(pub_key_bits)

# Then verify the Data packet using it
_, _, _, sig_ptrs = enc.parse_data(data_wire)
if sec.verify_ed25519(pub_key, sig_ptrs):
    print('Data verified')
else:
    print('Data not verified')
