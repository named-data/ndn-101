# Storage

Persistent storage is a key component of application functionality. In the NDN philosophy, highly available storage is provided as part of the network infrastructure. This allows applications to store data in the network, and to retrieve it from the network, without needing to rely on a separate storage service.

Generally speaking, there are three kinds of storage services in NDN. We describe each of these in further detail below.

- **Application Storage**: storage used by a particular application instance.
- **Data Repository**: a persistent general-purpose storage deployed in the network.
- **Content Store**: a passive cache configured in all NDN forwarders.

!!! info "General purpose storage"

    By design, NDN data stores are typically not application-specific, being provided as a service by the network infrastructure. This is in contrast to traditional cloud storage services, which are provided by third-party vendors and require applications to adapt to their specific APIs. Since data is secured independently of the transport and storage, the stored data is always secured at rest and in transit.

## Application Storage

Individual NDN applications typically require local storage for the data at a particular instance. This may include data that has been produced by the application, or data that has been fetched from the network. The application storage is typically managed by the application itself, and is not shared with other applications.

NDN libraries provide APIs for applications to store and retrieve data from local storage using the name. The storage itself may be implemented using memory or disk, and may store either the raw Data packets or the application-specific data structures.

=== "ndn-cxx"

    ``` c++
    --8<-- "snippets/storage/ims.cpp"
    ```

## Data Repository

Imagine the following scenario: an application uses some public _online storage_ to store its data.
To make sure the online storage stores the data faithfully, every uploaded file is signed.
The application provider does not need to operate the storage, nor do they need to pay for it:
the users will use their own quota and pay themselves.
To make sure data are available in case when the storage is down, users also have local copies of their data.

In this scenario, the role of the online storage plays a role similar to a Repo in NDN networks in some aspects but different in others.

- The similarities
    - General-purpose: the storage is not designed for specific application and not operated by application teams.
    The storage do not run application logic.
    - Untrusted: the storage is not trusted in the application's trust domains.
    It has its own trust relationship with producers who upload data to it, but this is not related to the application.
    The storage is not allowed to produce any data for the application.
    - Rendezvous point: when peers cannot be online simultaneously, the repo makes data available.
- The differences
    - The cloud storage has its own API.
    However, in the NDN world, data fetching is done by stardard Interest-Data exchange.
    Data consumers will notice the existence of Repo, ideally.
    - Different cloud providers typically cannot collaborate with each other,
    and the application developers have to pick some providers and adapt for them.
    NDN applications do not have to adapt for specific Repo providers.

## Content Store

The content store is an ephemeral cache in each NDN forwarder in the network, which stores the most recently or frequently requested data. Unlike the other storage types described above, the application does not exercise any control over the data stored in the content store. Further the content store does not provide any guarantess on cache eviction or availability, and thus should not be relied upon for long-term storage.

!!! warning "Data Immutability"

    Since any forwarder in the network may cache data for any duration of time, applications must not rely on a given Data packet eventually being unavailable. Each Data packet must be treated as immutable and potentially available forever, and thus names must not be reused.

!!! tip "Clearing the content store"

    During application development, the content store may lead to unexpected behavior, e.g. data that has not been produced yet may be available from a previous test run. In such situations, you may want to clear the cache using the `nfdc` command-line tool.

    ```bash
    nfdc cs erase /<prefix>  # erase all cached data under a prefix
    ```
