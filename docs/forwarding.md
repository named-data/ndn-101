# Forwarding Plane

!!! warning "This page is under construction."

NDN uses a stateful forwarding plane[@cc2013stateful] that maintains several tables at forwarders. This is in contrast to the stateless forwarding plane of IP, which does not maintain any per-packet state. The stateful forwarding plane of NDN enables Data multicast and caching, along with other features such as privacy, loop detection, network-layer congestion control[@icn2019congestion] and DoS protection[@icccn2013ddos].

Each instance of NFD in an NDN network maintains several tables. Some of these tables store per-packet state, thus making the forwarding plane stateful. These tables are described briefly in the following sections.

!!! info "Further Reading"

    If you are interested in the implementation details of NFD, please refer to the [NFD Developer Guide](https://named-data.net/publications/techreports/nfd-developer-guide/).

## Pending Interest Table (PIT)

The PIT is the most important table in the forwarding plane, and it provides the
basic support for the _pull_ model of communication in NDN.

When an instance of NFD receives an Interest, it stores a **PIT entry** in this table.
Each PIT entry contains the following information.

  - The name of the Interest along with any selectors.
  - The incoming face on which the Interest was received (**in-record**).
  - The outgoing face(s) on which the Interest was forwarded (**out-record**).
  - The time at which the Interest will expire (lifetime).

On receiving a Data packet, NFD performs the following steps.

  - Looks up the PIT for an entry matching the Data packet.
  - If such an entry is found, the Data packet is forwarded on the incoming face
    of the PIT entry, and the PIT entry is removed from the table.
  - If no matching PIT entry is found, the Data packet is dropped.

The PIT entry is also dropped if the Interest times out before a matching Data packet is received.

!!! tip "One-Interest One-Data"

    A fundamental principle of NDN is that one outgoing Interest can bring back at most one Data packet.
    This is enforced by the PIT, since the PIT entry is removed from the table as soon as a matching
    Data packet is received and forwarded to the incoming face.

!!! tip "Breadcrumb Trail"

    In an NDN network containing multiple forwarders, PIT entries for an Interest serve as a breadcrumb trail
    that the Data packet follows back to the consumer. As a result, no source address is required in the
    Interest packet for sending the Data packet back to the consumer.

!!! info "Implementation of PIT"

    For efficiency, forwarders may implement the PIT using tree-based data structures
    or hash tables. The entry expiration is typically implemented using priority queues.

### Data Multicast

The per-packet statefulness of the PIT directly enables Data multicast by allowing a single
Data packet to be forwarded to multiple consumers that have expressed an Interest
in the same data.

When NFD receives an Interest, it first looks up the PIT for an entry matching the Interest.
If such an entry is found, the Interest is aggregated with the existing entry, by appending
an in-record to the entry for the incoming face of the new Interest. The Interest is then not
forwarded further.

When a matching Data packet is received, it is forwarded on all the incoming faces of
the PIT entry. As a result, multiple Interests are satisfied with a single Data packet,
thus realizing Data multicast.

!!! tip "Multicast and Interest Selectors"

    Interests can generally be aggregated only if they have the same name and selectors.
    For instance, two Interests having the same name but different values for the `MustBeFresh`
    selector cannot be aggregated, since they are potentially requesting different Data packets.

### Consumer Privacy

Since the PIT stores the incoming face of each Interest, the outgoing Interest does not
need to contain any information about the incoming face. This enables consumer privacy in
NDN, by ensuring that Interest packets cannot be used to identify the original sender.

### Loop Detection

The PIT also lets NFD detect and prevent looping Interests. Each Interest in NDN carries a
randomly generated nonce, which is stored in the PIT entry along with the Interest name.
When NFD receives an Interest, it first looks up the PIT for an entry matching the Interest.
If such an entry is found including a matching nonce, then the incoming Interest is dropped.

!!! tip "Longer Loops"

    While the PIT prevents some types of looping Interests, it fails to detect longer loops,
    since an Interest may be satisfied by a Data packet before it loops back to the same
    forwarder. To detect such looping Interests, NFD uses a separate table called the
    **Dead Nonce List**, which stores nonces of recently satisfied Interests.
