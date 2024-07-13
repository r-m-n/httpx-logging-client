import asyncio
from httpx_logging_client import AsyncLoggingClient, LoggingClient

import structlog


structlog.configure(
    processors=[structlog.processors.JSONRenderer(sort_keys=True, indent=4)]
)


async def main():
    async with AsyncLoggingClient() as cl:
        await cl.get("https://httpbin.org/uuid")


def main2():
    with LoggingClient() as cl:
        cl.get("https://httpbin.org/uuid")


if __name__ == "__main__":
    asyncio.run(main())
    main2()
