import { Component, Data, Name } from '@ndn/packet';
import { Encoder } from '@ndn/tlv';
import { toHex, toUtf8 } from '@ndn/util';
import { Certificate, Ed25519, generateSigningKey, ValidityPeriod } from '@ndn/keychain';

// Generate trust anchor of admin
const adminIdentityName = new Name('/lab/admin');
const [adminSelfSigner, adminVerifier] = await generateSigningKey(adminIdentityName, Ed25519);
const anchor = await Certificate.selfSign({
  privateKey: adminSelfSigner,
  publicKey: adminVerifier,
});
const adminSigner = adminSelfSigner.withKeyLocator(anchor.name);
const anchorWire = Encoder.encode(anchor.data);
console.log(`Admin trust anchor name: ${anchor.name.toString()}`);
console.log(`Admin trust anchor hex: ${toHex(anchorWire)}`);
console.log('');
// The following line create the verifier from certificate
// const anchor = Certificate.fromData(Decoder.decode(anchorWire, Data));
// const adminVerifier = await createVerifier(anchor, {algoList: [Ed25519]});

// Generate the student's key and issue him a certificate
const stuIdentityName = new Name('/lab/student/xinyu.ma');
const [stuSelfSigner, stuVerifier] = await generateSigningKey(stuIdentityName, Ed25519);
const stuCert = await Certificate.issue({
  issuerPrivateKey: adminSigner,
  publicKey: stuVerifier,
  issuerId: new Component(8, 'admin'),
  // Equivalent to the following:
  // validity: new ValidityPeriod(Date.now(), Date.now() + 365 * 86400000),
  validity: ValidityPeriod.daysFromNow(365),
});
const stuSigner = stuSelfSigner.withKeyLocator(stuCert.name);
const stuCertWire = Encoder.encode(stuCert.data);
console.log(`Student certificate name: ${stuCert.name.toString()}`);
console.log(`Student certificate hex: ${toHex(stuCertWire)}`);
console.log('');

// Sign the paper's data with the student's certificate
const data = new Data(
  new Name('/lab/paper/ndn/change/1'),
  Data.FreshnessPeriod(10000),
  toUtf8('Hello, NDN!'),
);
await stuSigner.sign(data);
const dataWire = Encoder.encode(data);
console.log('Data:', toHex(dataWire));
