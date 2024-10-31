import typing

import httpx
from httpx import (
    ASGITransport,
    WSGITransport,
)
from httpx._config import (
    DEFAULT_LIMITS,
    Limits,
    Proxy,
)
from httpx._types import (
    CertTypes,
    VerifyTypes,
)

from httpx_structlog.transport import (
    AsyncHTTPLoggingTransport,
    HTTPLoggingTransport,
)


class LoggingClient(httpx.Client):
    def _init_transport(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        transport: httpx.BaseTransport | None = None,
        app: typing.Callable[..., typing.Any] | None = None,
        trust_env: bool = True,
    ) -> httpx.BaseTransport:
        if transport is not None:
            return transport

        if app is not None:
            return WSGITransport(app=app)

        return HTTPLoggingTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
        )

    def _init_proxy_transport(
        self,
        proxy: Proxy,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        trust_env: bool = True,
    ) -> HTTPLoggingTransport:
        return HTTPLoggingTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
            proxy=proxy,
        )


class AsyncLoggingClient(httpx.AsyncClient):
    def _init_transport(
        self,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: httpx.Limits = DEFAULT_LIMITS,
        transport: httpx.AsyncBaseTransport | None = None,
        app: typing.Callable[..., typing.Any] | None = None,
        trust_env: bool = True,
    ) -> httpx.AsyncBaseTransport:
        if transport is not None:
            return transport

        if app is not None:
            return ASGITransport(app=app)

        return AsyncHTTPLoggingTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
        )

    def _init_proxy_transport(
        self,
        proxy: Proxy,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        http1: bool = True,
        http2: bool = False,
        limits: Limits = DEFAULT_LIMITS,
        trust_env: bool = True,
    ) -> AsyncHTTPLoggingTransport:
        return AsyncHTTPLoggingTransport(
            verify=verify,
            cert=cert,
            http1=http1,
            http2=http2,
            limits=limits,
            trust_env=trust_env,
            proxy=proxy,
        )
