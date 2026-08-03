from ndn.appv2 import NDNApp, PktContext, ReplyFunc
from ndn.encoding import BinaryStr, FormalName, Name

# Connect to the local forwarder over a Unix socket
app = NDNApp()
keychain = app.default_keychain()


# Register a prefix, and call on_interest when a matching Interest is received
@app.route("/edu/ucla/cs/118/notes")
def on_interest(
    name: FormalName,
    app_param: BinaryStr | None,
    reply: ReplyFunc,
    context: PktContext,
):
    print(f"Received Interest packet for {Name.to_str(name)}")

    # Create the content bytes for the Data packet
    content = b"Hello, NDN!"

    # Create and sign the Data packet
    data = app.make_data(
        name, content, keychain.get_signer({}), freshness_period=10000
    )

    # Send the Data packet back to the network
    reply(data)


if __name__ == "__main__":
    app.run_forever()
