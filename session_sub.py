import asyncio
from copilot import CopilotClient, PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    # Await the session creation
    session = await client.create_session({
        "model": "gpt-4.1",
        "on_permission_request": PermissionHandler.approve_all
    })
    
    # Now you can subscribe to events
    unsubscribe = session.on(lambda event: print(f"Event: {event.type}"))
    
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})
    print(f"Response: {response.data.content}")

    await client.stop()

asyncio.run(main())