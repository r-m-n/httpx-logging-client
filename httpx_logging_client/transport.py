import time

import httpx
import structlog
from httpx import (
    Request,
    Response,
)
from structlog.types import FilteringBoundLogger

logger = structlog.get_logger()


def log_bind_request(
    log: FilteringBoundLogger, request: Request
) -> FilteringBoundLogger:
    return log.bind(
        method=request.method,
        path=request.url.path,
        host=request.url.netloc.decode(),
        request_headers=dict(request.headers.items()),
        request_body=request.content.decode(),
        request_query=request.url.query.decode(),
    )


def log_bind_response(
    log: FilteringBoundLogger, response: Response
) -> FilteringBoundLogger:
    return log.bind(
        response_status=response.status_code,
        response_headers=dict(response.headers.items()),
    )


class HTTPLoggingTransport(httpx.HTTPTransport):
    def handle_request(self, request: Request) -> Response:
        log = log_bind_request(logger, request)
        start_time = time.perf_counter()
        try:
            response = super().handle_request(request)
            end_time = time.perf_counter()
            log = log_bind_response(log, response)
            response.read()
            log.info(
                "httpx request",
                response_body=response.content.decode(),
                duration=end_time - start_time,
            )
            return response
        except httpx.HTTPError as exc:
            log.error("httpx http error", exc_info=True)
            raise exc


class AsyncHTTPLoggingTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(
        self,
        request: Request,
    ) -> Response:
        await request.aread()
        log = log_bind_request(logger, request)
        start_time = time.perf_counter()
        try:
            response = await super().handle_async_request(request)
            end_time = time.perf_counter()
            log = log_bind_response(log, response)
            await response.aread()
            log.info(
                "httpx request",
                response_body=response.content.decode(),
                duration=end_time - start_time,
            )
            return response
        except httpx.HTTPError as exc:
            log.error("httpx http error", exc_info=True)
            raise exc
