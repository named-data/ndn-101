# Research Testbed

!!! warning "This page is under construction."

The [NDN research testbed](https://named-data.net/ndn-testbed/) is a shared resource created for research purposes, that include software routers at several participating institutions, application host nodes, and other devices. The testbed is used for research and development of NDN software, and for experiments that require a shared NDN infrastructure. It is not intended for production use.

!!! tip "Connecting NFD to the Testbed"
    To connect your local NFD to the testbed, use the `ndn-autoconfig` tool. This tool uses the Find-Closest-Hub (FCH) service to find the closest testbed node, and creates a face from your local NFD to that node. It also configures the local NFD to use the testbed as a default route for Interests that do not match any local routes.

    ```bash
    nfd-start               # start local NFD
    ndn-autoconfig          # connect to the testbed
    ndnping /ndn/edu/ucla   # test the connection (optional)
    ```

## Obtaining a testbed certificate

The easiest way to obtain a testbed certificate is to use the NDNCERT client. To begin ensure that you have installed [NFD](https://docs.named-data.net/NFD/current/INSTALL.html) and [NDNCERT](https://github.com/named-data/ndncert).

You can now request a certificate from the testbed certificate authority.

```bash
# Start and connect your local NFD to the testbed
nfd-start
ndn-autoconfig

# Configure the NDNCERT client using the default configuration (if required)
sudo cp /usr/local/etc/ndncert/client.conf.sample /usr/local/etc/ndncert/client.conf

# Request a testbed certificate
ndncert-client
```

You will be prompted to select the CA. Choose index `0` to probe the NDN Testbed root CA.
```
Step 1: CA SELECTION
> Index: 0
>> CA prefix:/ndn
>> Introduction:
Please type in the CA's index that you want to apply or type in NONE
if your expected CA is not in the list:
```

The client will then prompt you to provide your email address for name assignment. If you use an email address from a domain that is part of the testbed, the client will redirect your request to the appropriate Site CA. Otherwise, you will be issued a certificate from the Testbed Root CA.
```
Step 2: Please provide information for name assignment
Please input: email
```

Next, provide the expected validity period for the certificate, which should be less than the maximum allowed by the CA.
```
Step 3: Please type in your expected validity period of your certificate.
Type the number of hours (168 for week, 730 for month, 8760 for year).
The CA may reject your application if your expected period is too long.
The maximum validity period allowed by this CA is 360 hours.
```

(Optional) If local keychain already has a key with same name, you need to select whether you want to certify an existing key, or creating a new key under the same name and certify it.
```
Step 4: KEY SELECTION
Index: 0
>> Key Name:  +->* /ndn/edu/ucla/alice/KEY/%BE%B1cqk%25%3D%20
Please type in the key's index that you want to certify
or type in NEW if you want to certify a new key:
```

The CA will now send a verification code to your email address (this code may sometimes be sent to your spam folder). Enter the code to complete the certificate request.
```
Step 4: Please provide parameters used for Identity Verification Challenge
Please input your verification code
```

If verification succeeds, the certificate will be issued and installed into your local ndnsec keychain.

```bash
# View all existing certificates
ndnsec list -c
```

## Prefix announcements

Once you have obtained a testbed certificate as described above, you can announce your data prefixes to testbed routing (NLSR). This allows other applications connected to the testbed to send Interests to your application.

A simple way to announce your prefix during debugging is to use the [ndn6-tools](https://github.com/yoursunny/ndn6-tools) package.

```bash
# Get the name of the certificate issued by NDNCERT and set it to default
# Certificates issed by NDNCERT are indicated as such in the name
ndnsec list -c
ndnsec set-default -c /ndn/edu/ucla/alice/KEY/%5C7%02%D6%A2%1E%CFo/NDNCERT/v=1709685136466

# Dump the newly obtained certificate to a file using ndnsec
ndnsec cert-dump /ndn/edu/ucla/alice/KEY/%5C7%02%D6%A2%1E%CFo/NDNCERT/v=1709685136466 > testbed.cert

# Make sure this certificate is available to consumers (NLSR)
ndn6-serve-certs testbed.cert

# Find the remote of the face connecting to the testbed
# e.g. udp4://131.179.196.48:6363
nfdc face list

# Send a prefix announcement to the testbed
ndn6-register-prefix-remote \
    -f udp4://131.179.196.48:6363 \
    -p /alice/test \
    -i /ndn/edu/ucla/alice

# If the above command returns a 200 status code, the prefix has been successfully announced
```

You can now register prefixes under the `/alice/test` namespace with your local NFD and be reachable from other nodes connected to the testbed.

## Connection from application

When a local NFD is not available, for example in web-based applications, the application may directly connect to a testbed node.
The [FCH service](https://fch.ndn.today) allows applications to find the geographically closest testbed node using the client's IP address. No security configuration is required to send Interests to the testbed, as illustrated in the following example.

=== "NDNts"

    ``` typescript
    --8<-- "snippets/testbed/app-consumer.ts"
    ```
