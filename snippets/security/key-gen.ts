import { Data, Name } from '@ndn/packet';
import { Decoder, Encoder } from '@ndn/tlv';
import { toHex, toUtf8 } from '@ndn/util';
import { Ed25519, generateSigningKey } from '@ndn/keychain';

// Generate key pairs (Recommend ECDSA and Ed25519 for EdDSA)
const identityName = new Name('/edu/ucla/xinyu.ma');
const [signer, verifier] = await generateSigningKey(identityName, Ed25519);
// Sign a Data with it
const data = new Data(
  new Name('/edu/ucla/cs/118/notes'),
  Data.FreshnessPeriod(10000),
  toUtf8('Hello, NDN!'));
await signer.sign(data);
// Print the Data wire
const wire = Encoder.encode(data);
console.log('Data:', toHex(wire));

// Export public keys
const publicKeyBits = verifier.spki!;
console.log('Public Key bits:', toHex(publicKeyBits));
// Importing a public key in NDNts is very complicated
// so I recommend to use a certificate instead.
// I will show you how to do it later.

// Then verify the Data packet using it
const decodedData = Decoder.decode(wire, Data); // Be the same as `data`
try {
  await verifier.verify(decodedData);
  console.log('Data verified');
} catch {
  console.log('Data not verified');
}
