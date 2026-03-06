import asyncio
from copilot import CopilotClient, PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session({
        "model": "gpt-4.1",
        "on_permission_request": PermissionHandler.approve_all,
        "mcp_servers": {
            "github": {
                "type": "http",
                "url": "https://api.githubcopilot.com/mcp/"
            }
        }
    })

    tool_event_seen = False

    def on_event(event):
        nonlocal tool_event_seen
        event_type = str(getattr(event, "type", ""))
        print(f"Event: {event_type}")
        if "tool" in event_type.lower() or "mcp" in event_type.lower():
            tool_event_seen = True

    unsubscribe = session.on(on_event)

    response = await session.send_and_wait({
        "prompt": (
            "Use the configured GitHub MCP server and perform one tool call. "
            "If successful, reply exactly: MCP_OK. "
            "If not, reply: MCP_FAIL and the reason."
        )
    })

    text = str(getattr(response.data, "content", ""))
    print("Assistant:", text)

    if tool_event_seen or "MCP_OK" in text:
        print("MCP connection test: PASS")
    else:
        print("MCP connection test: FAIL")

    unsubscribe()
    await client.stop()

asyncio.run(main())