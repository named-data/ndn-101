from ndn.app import NDNApp
from ndn.encoding import Name

# Connect to the local forwarder over a Unix socket
app = NDNApp()

async def main():
    try:
        data_name, meta_info, content = await app.express_interest("/edu/ucla/cs/118/notes")

        # Received a Data packet
        print(f'Received Data Name: {Name.to_str(data_name)}')
        print(meta_info)
        print(bytes(content) if content else None)

    except InterestNack as e:
        # Received a Nack (negative acknowledgement)
        print(f'Nacked with reason={e.reason}')
    except InterestTimeout:
        # The Interest has timed out
        print(f'Timeout')
    except InterestCanceled:
        # Connection to the local NDN forwarder is broken
        print(f'Canceled')
    except ValidationFailure:
        # Security validation failed for the data
        print(f'Data failed to validate')

    finally:
        # Disconnect from the local forwarder
        app.shutdown()

if __name__ == '__main__':
    app.run_forever(after_start=main())