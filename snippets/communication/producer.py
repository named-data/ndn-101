from ndn.app import NDNApp
from ndn.encoding import BinaryStr, FormalName, InterestParam, Name

# Connect to the local forwarder over a Unix socket
app = NDNApp()


# Register a prefix, and call on_interest when a matching Interest is received
@app.route("/edu/ucla/cs/118/notes")
def on_interest(
    name: FormalName, param: InterestParam, _app_param: BinaryStr | None
):
    print(f"Received Interest packet for {Name.to_str(name)}")

    # Create the content bytes for the Data packet
    content = b"Hello, NDN!"

    # Sign and send the Data packet back to the network
    app.put_data(name, content=content, freshness_period=10000)


if __name__ == "__main__":
    app.run_forever()
