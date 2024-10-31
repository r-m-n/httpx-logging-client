Сustom httpx client that logs all requests and responses with structlog.

Usage

```python
from httpx_structlog import AsyncLoggingClient, LoggingClient

# configure structlog
# structlog.configure(
#     processors=[structlog.processors.JSONRenderer(sort_keys=True, indent=4)]
# )

# Sync client
with LoggingClient() as client:
    client.get("https://httpbin.org/uuid")


# Async client
async with AsyncLoggingClient() as client:
    await client.get("https://httpbin.org/uuid")
```

Log example

```json
{
    "duration": 0.49533109995536506,
    "event": "httpx request",
    "host": "httpbin.org",
    "method": "GET",
    "path": "/uuid",
    "request_body": "",
    "request_headers": {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "connection": "keep-alive",
        "host": "httpbin.org",
        "user-agent": "python-httpx/0.27.0"
    },
    "request_query": "",
    "response_body": "{\n  \"uuid\": \"36a2c551-8632-4712-8b56-d3e21819c04e\"\n}\n",
    "response_headers": {
        "access-control-allow-credentials": "true",
        "access-control-allow-origin": "*",
        "connection": "keep-alive",
        "content-length": "53",
        "content-type": "application/json",
        "date": "Sat, 13 Jul 2024 12:22:17 GMT",
        "server": "gunicorn/19.9.0"
    },
    "response_status": 200
}
```
