import asyncio
from copilot import CopilotClient, PermissionHandler
from copilot.generated.session_events import SessionEvent, SessionEventType


async def main():
    client = CopilotClient()
    await client.start()

    # Await the session creation
    session = await client.create_session({
        "model": "gpt-4.1",
        "on_permission_request": PermissionHandler.approve_all
    })

    # Define event handler
    def handle_event(event):
        if event.type == SessionEventType.SESSION_IDLE:
            print("Session is idle")
        elif event.type == SessionEventType.ASSISTANT_MESSAGE:
            print(f"Message: {event.data.content}")
        else:
            print(f"Event: {event.type}")

    # Subscribe to all events
    unsubscribe = session.on(handle_event)

    # Send a prompt to trigger events
    response = await session.send_and_wait({"prompt": "What is 2 + 2?"})
    print(f"\nFinal response: {response.data.content}")

    # Unsubscribe when done
    unsubscribe()

    await client.stop()

# Run the async main function
asyncio.run(main())