from datetime import datetime, timedelta, timezone
import ndn.encoding as enc
import ndn.security as sec
import ndn.app_support.security_v2 as secv2
from Cryptodome.PublicKey import ECC
from Cryptodome.Random import get_random_bytes


# Generate trust anchor of admin
admin_priv = ECC.generate(curve='ed25519')
admin_pub = admin_priv.public_key()
admin_pub_bits = admin_pub.export_key(format='DER')
admin_identity_name = enc.Name.from_str('/lab/admin')
# Key name is <IdentityName>/KEY/<keyId>, here we use random value as key ID.
# You can also use timestamp, sequencial number, or hash.
admin_key_name = enc.Name.normalize(
    admin_identity_name + ['KEY', enc.Component.from_bytes(get_random_bytes(8))])
# Self signer is used to sign the self-signed certificate only.
admin_self_signer = sec.Ed25519Signer(
    admin_key_name, admin_priv.export_key(format='DER'))
anchor_name, anchor = secv2.self_sign(
    admin_key_name, admin_pub_bits, admin_self_signer)
# We create a new signer with this certificate's name for further use
admin_signer = sec.Ed25519Signer(
    anchor_name, admin_priv.export_key(format='DER'))
print(f'Admin trust anchor name: {enc.Name.to_str(anchor_name)}')
print(f'Admin trust anchor hex: {bytes(anchor).hex()}')
print()

# Generate the student's key and issue him a certificate
stu_priv = ECC.generate(curve='ed25519')
stu_pub = stu_priv.public_key()
stu_pub_bits = stu_pub.export_key(format='DER')
stu_identity_name = enc.Name.from_str('/lab/student/xinyu.ma')
stu_key_name = enc.Name.normalize(
    stu_identity_name + ['KEY', enc.Component.from_bytes(get_random_bytes(8))])
stu_cert_name, stu_cert = secv2.new_cert(
    stu_key_name,
    'admin',
    stu_pub_bits,
    admin_signer,
    start_time=datetime.now(timezone.utc),
    end_time=datetime.now(timezone.utc) + timedelta(days=365),
)
stu_signer = sec.Ed25519Signer(
    stu_cert_name, stu_priv.export_key(format='DER'))
print(f'Student certificate name: {enc.Name.to_str(stu_cert_name)}')
print(f'Student certificate hex: {bytes(stu_cert).hex()}')
print()

# Sign the paper's data with the student's certificate
data_wire = enc.make_data(
    name='/lab/paper/ndn/change/1',
    meta_info=enc.MetaInfo(freshness_period=10000),
    content=b'Hello, NDN!',
    signer=stu_signer
)
print('Data:', data_wire.hex())
