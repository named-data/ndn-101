---
title: Trust Model
---

# Data-centric Trust in NDN

This article provides a brief overview of the data-centric trust model of NDN.

The key feature of NDN that enables systematic and provable data centric security is the semantic name that identifies each object in an NDN application. By encoding semantics into the name of an object, applications can establish trust relations directly based on data names, rather than using ad-hoc and often manually configured Access Control Lists (ACLs).

The data centric trust model has two key requirements - **identity** and **policy**. We first describe these components in detail before explaining the NDN trust model with an example.

## Identity

To enable secure communication in any network,

1. Each entity must be uniquely identifiable.
2. All communicating entities should be able to authenticate each other.

In the NDN trust model, each entity is identified with a unique name. The key component of the data-centric trust model is that this name describes semantics about the entity. The structuring of NDN names can be considered to be similar to, and optionally be based on the existing DNS name hierarchy.

An example of a semantic name hierarchy partially based on existing DNS names is shown below.
The exact name hierarchy to use may depend on application semantics, as described in later sections.

```bash
# Structured NDN identity name for an organization.
/edu/ucla

# A nested sub-namespace inside UCLA to represent a "department".
# In this case, we encode the organizational semantics into the identity.
/edu/ucla/cs
/edu/ucla/remap

# A sub-namespace inside a department identifying an individual person.
/edu/ucla/cs/faculty/lixia
/edu/ucla/cs/students/varun
/edu/ucla/remap/faculty/jeff

# A separate namespace identifying individual smart devices.
/edu/ucla/cs-building/floor-3/room-372/door
/edu/ucla/cs-building/floor-5/room-514/light/2
```

Entities in NDN authenticate each other using heirarchical certificates. Each entity is provisioned with a private key that is certified by another entity higher up in the hierarchy. On receiving data from another entity, the consumer can authenticate the other entity using this certificate.

Each organization and application gains full control over their trust model by having a local trust anchor and delegating authority to issue certificates. The example below shows how the certificates hierarchy may be established in the UCLA organization.

```bash
# In this example, each line represents a certificate issued to an
# entity by another entity. The notation used is `identity <= issuer`

# The trust anchor key is the root of all trust.
# This certificate is self-signed and must be well-known to all entities.
/edu/ucla <= /edu/ucla

# The root key is used to certify all departments.
/edu/ucla/cs     <= /edu/ucla
/edu/ucla/remap  <= /edu/ucla

# Departments in turn certify all staff and students.
/edu/ucla/cs/faculty/lixia    <= /edu/ucla/cs
/edu/ucla/cs/students/varun   <= /edu/ucla/cs
/edu/ucla/remap/faculty/jeff  <= /edu/ucla/remap

# Departments also certify all devices that are owned by them.
/edu/ucla/cs-building/floor-3/room-372/door     <= /edu/ucla/cs
/edu/ucla/cs-building/floor-5/room-514/light/2  <= /edu/ucla/cs
```

Each NDN certificate is NDN data itself, and identifies signer of the certificate using a `KeyLocator` field.
As a result, consumers can directly fetch the chain of certificates needed to verify a given data till they reach
a root of trust.

In the above example, if `jeff` receives a data object `website` from `lixia`,

1. `lixia` signs the data with the `/edu/ucla/cs/faculty/lixia` key, received by `jeff`.
2. `jeff` fetches the `/edu/ucla/cs/faculty/lixia <= /edu/ucla/cs` certificate using the `KeyLocator` in the data.
4. `jeff` verifies the signature on the data with the public key in the certificate.
5. `jeff` fetches the `/edu/ucla/cs <= /edu/ucla` certificate using the `KeyLocator` in the certificate.
6. `jeff` verifies the signature on the first certificate.
7. `jeff` verifies the second certificate, which is signed by a known trust anchor.
8. The chain of verification is now complete, and `jeff` has successfully authenticated that `lixia` originally produced the data.

``` mermaid
flowchart TD
    /edu/ucla -->|signs| /edu/ucla/cs
    /edu/ucla -->|signs| /edu/ucla/remap

    /edu/ucla/cs -->|signs| /edu/ucla/cs/students/varun
    /edu/ucla/cs -->|signs| /edu/ucla/cs/faculty/lixia -->|signs| lws([/edu/ucla/cs/faculty/lixia/website])
    /edu/ucla/remap -->|signs| /edu/ucla/remap/faculty/jeff

    lws -. fetched by .-> /edu/ucla/remap/faculty/jeff
```

!!! tip "The WebPKI trust model"

    In the traditional WebPKI trust model, the unique identity is typically provided by the DNS system, and authentication is provided by one or more "trusted" certificate authorities. This means, however, that all trust between communicating entities depends on the implicit trust they have in these certificate authorities, typically by virtue of having certificates pre-installed in the operating system.
