from ndn.appv2 import NDNApp, pass_all
from ndn.encoding import Name
from ndn.types import (
    InterestCanceled,
    InterestNack,
    InterestTimeout,
    ValidationFailure,
)

# Connect to the local forwarder over a Unix socket
app = NDNApp()


async def main():
    try:
        data_name, content, pkt_context = await app.express(
            "/edu/ucla/cs/118/notes", validator=pass_all
        )

        # Received a Data packet
        print(f"Received Data Name: {Name.to_str(data_name)}")
        print(pkt_context["meta_info"])
        print(bytes(content) if content else None)

    except InterestNack as e:
        # Received a Nack (negative acknowledgement)
        print(f"Nacked with reason={e.reason}")
    except InterestTimeout:
        # The Interest has timed out
        print("Timeout")
    except InterestCanceled:
        # Connection to the local NDN forwarder is broken
        print("Canceled")
    except ValidationFailure:
        # Security validation failed for the data
        print("Data failed to validate")

    finally:
        # Disconnect from the local forwarder
        app.shutdown()


if __name__ == "__main__":
    app.run_forever(after_start=main())
