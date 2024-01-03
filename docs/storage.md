# Storage

!!! warning "This page is under construction."

In NDN, there are several kinds of storages, including
- _Content store_: a passive cache configured in all NDN forwarders.
    Deployed by NDN network providers.
- _Repo_: a persistent general-purpose storage deployed in the network.
    They are deployed and maintained by third party indepenend of the application users or developers.
- _Application storage_: storages used by specific applications.
    They are maintained by the software developers and operated by users or service providers.

## Content Store (passive cache)

Content store is part of an NDN forwarder. Please see [Forwarding Plane](forwarding.md#content-store).

## Repo (general persistent storage)

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
