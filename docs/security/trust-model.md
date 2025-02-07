---
title: Trust Model
---

# Data-centric Trust in NDN

This article provides a brief overview of the data-centric trust model of NDN.

The key feature of NDN that enables systematic and provable data centric security is the semantic name that identifies each object. NDN applications establish trust relations directly based on data names, which eliminates the need for manually configured roles and ACLs.

The data-centric trust model of NDN is based two components. When communicating with someone, one needs to know,

1. **Identity**: Who am I talking to?
2. **Policy**: What are they allowed to say?

We describe these components in detail and explain the NDN trust model with an example.

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
/edu/ucla/facilities/eng6/floor-3/room-372/door
/edu/ucla/facilities/eng6/floor-5/room-514/door
/edu/ucla/facilities/eng6/floor-5/room-514/light/2
```

``` mermaid
flowchart TD
    ucla --> cs
    ucla --> remap

    cs --> f1[faculty] --> lixia{{lixia}}
    cs --> students --> varun{{varun}}
    remap --> f2[faculty] --> jeff{{jeff}}

    ucla --> facilities --> eng6
    eng6 --> floor-3 --> room-372 --> door{{door}}
    eng6 --> floor-5 --> room-514 --> door2{{door}}
    room-514 --> light --> two{{2}}
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
/edu/ucla/facilities/eng6/floor-3/room-372/door     <= /edu/ucla/cs
/edu/ucla/facilities/eng6/floor-3/room-514/door     <= /edu/ucla/cs
/edu/ucla/facilities/eng6/floor-5/room-514/light/2  <= /edu/ucla/cs
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

    /edu/ucla/cs -->|signs| varun{{/edu/ucla/cs/students/varun}}
    /edu/ucla/cs -->|signs| lixia{{/edu/ucla/cs/faculty/lixia}} -->|signs| lws([/edu/ucla/cs/faculty/lixia/website])
    /edu/ucla/remap -->|signs| jeff{{/edu/ucla/remap/faculty/jeff}}

    lws -. fetched by .-> jeff
```

!!! tip "Identity in WebPKI"

    In the traditional WebPKI trust model, the unique identity is typically provided by the DNS system, and authentication is provided by one or more "trusted" certificate authorities. This means, however, that all trust between communicating entities depends on the implicit trust they have in these certificate authorities, typically by virtue of having certificates pre-installed in the operating system.

## Trust Policy

Once every communicating entity has an identity, consumers can know **who** they are talking to. However, they still need to know **what** the other entity can say. This information is systematically encoded in a *trust policy* defined by the application.

In NDN, a **trust schema** defines an application or organization's trust policy using a trust language such as [Light Versec](https://python-ndn.readthedocs.io/en/latest/src/lvs/lvs.html). One or more trust languages are supported by all major NDN implementations.

The trust schema defines which producer (by name) is allowed to generate what data. Typically, the trust schema is defined hierarchically, utilizing the name semantics of the application.

To illustrate the usage of a name-based trust policy, we utilize the same UCLA example described above. Let us assume that the following policy must be enforced by the organization.

1. All CS faculty can open all doors in the Engineering 6 building.
2. Everyone in the CS department can turn on lights in Engineering 6.
3. All faculty in UCLA can open doors on Floor 5 in Engineering 6.

Such a trust policy can be written as a simple NDN trust schema as described below.
Note that the pseudo-sytax is very similar to Light Versec, but is described in a verbose
format for ease of understanding.

```golang
// Each line below is a policy "rule" - a definition of who can say what.
// The pseudo syntax is similar to Light Versec and describes:
//
//   #rule_name: /what/data/is/this <= /who/can/say/this
//
// We must first define the certification hierarchy in the application.
// We start by definining the root of trust of the organization.
#ucla: /"edu"/"ucla"

// Rules may now refer to previously defined rules.
//
// Here, we define the name structure of a department, and declare that it
// must be signed by the root of trust. The #KEY component refers to NDN's
// pre-defined certificate naming convention.
//
// Since `dept` is not in quotes, it refers to a wildcard name component.
// Thus, UCLA can now sign new departments with the root key without changing
// the organization-wide trust policy.
#department: #ucla/dept/#KEY <= #ucla/#KEY

// The next rule defines name structure for students and faculty, and declares
// that these must be signed by the department they belong to.
//
// In this rule, notably, since #department is used in both the rule and the
// signer definition, the wildcard components must match during verfication.
// This means that the `/edu/ucla/remap` key cannot sign the certificate
// for /edu/ucla/cs/students/varun
//
// Note that this structure is not rigid. For example, additional rules may
// define some rule exceptions, such as where certain faculty certificates
// may be signed by other departments.
#students: #department/"students"/name/#KEY <= #department
#faculty: #department/"faculty"/name/#KEY <= #department

// Finally we define the naming structure for devices in UCLA facilities.
// To allow one room to have multiple lights, we define an unnamed wildcard
// component with `_`, which can match anything.
#room: #ucla/"facilities"/building/floor/room
#door: #room/"door"
#light: #room/"light"/_

// We can now define our actual device-control trust policy.
//
// "All CS faculty can open all doors in the Engineering 6 building."
//
// To define this policy, we restrict the `building` variable to a particular
// value, and define the entities allowed to say the "open" command by
// restricting the `dept` variable in the signers.
#cs_faculty: #faculty & { dept: "cs" }
#policy1: #door/"open" & { building: "eng6" } <= #cs_faculty

// "Everyone in the CS department can turn on lights in Engineering 6."
//
// We use two wildcards for the "cs_all" rule, the first to allow
// any type of person (student or faculty), and the second to allow any
// name. There are many different ways to write the same rule in a trust
// language, and the rule below is only representative.
#cs_all: #department/_/_/#KEY & { dept: "cs" }
#policy2: #light/"on" & { building: "eng6" } <= #cs_all

// "All faculty in UCLA can open doors on Floor 5 in Engineering 6."
//
// Once the naming structure is well-defined, additional complex rules
// can be easily added using the trust schema rules syntax.
#policy3: #door/"open" & { building: "eng6", floor: "floor-5" } <= #faculty
```

Once a trust policy is defined as a trust schema, NDN client libraries can automatically enforce the policy on all received data. For example, if the schema above is installed in all devices in UCLA, a door in Engineering 6 can automatically verify if the entity sending an "open" command is authorized to perform this action.

Two important features of a schematized trust policy may be noted below.

1. Additional certificates can now be issued without modifying the policy. For example, new students in the CS department can be issued a certificate with the correct naming structure, and they are automatically granted access to use lights in the E6 building. Schematizing the trust policy eliminates the need to maintain complicated ACLs.
2. The trust policy establishes relations directly between users and the devices, without the requirement of a trusted identity provider. This eliminates the single point of failure, and the system continues to function even when disconnected from the public internet, e.g. in ad-hoc or air-gapped scenarios.
